<script setup>
// 🔧 导入 Vue 3 的核心功能
import {h, nextTick, onMounted, reactive, ref} from "vue";
// 🎨 导入 Ant Design Vue 的图标组件
import {InfoCircleOutlined, PlusOutlined, QuestionCircleOutlined, SearchOutlined} from "@ant-design/icons-vue";
// 📝 导入子组件：车辆信息表单
import VehicleInfoForm from "./components/VehicleInfoForm.vue";
// 🌐 导入 HTTP 请求工具
import {HTTP} from "../../api/service.js";
// 🧭 导入路由器（用于页面跳转）
import router from "../../router.js";

// 📊 定义表格列配置（表头信息）
const columns = ref([
  {
    title: '入站时间',           // 列标题
    dataIndex: 'createdAt',      // 对应数据字段名
    key: 'createdAt',            // 唯一标识
    sorter: (a, b) => a.createdAt.localeCompare(b.createdAt), // 排序函数
    sortDirections: ['descend', 'ascend'], // 排序方向
    width: 180                   // 列宽度
  },
  {
    title: "探测站",
    dataIndex: "recordStation",
    key: "recordStation",
    sorter: (a, b) => a.recordStation.localeCompare(b.recordStation),
    sortDirections: ['descend', 'ascend'],
    width: 160
  },
  {
    title: "行车方向",
    dataIndex: "travelDirection",
    key: "travelDirection",
    sorter: (a, b) => a.travelDirection.localeCompare(b.travelDirection),
    sortDirections: ['descend', 'ascend'],
    width: 120
  },
  {
    title: '车次信息',
    dataIndex: 'vehicleInfo',
    key: 'vehicleInfo',
    sorter: (a, b) => a.vehicleInfo.localeCompare(b.vehicleInfo),
    sortDirections: ['descend', 'ascend'],
    width: 120
  },
  {
    title: "车号信息",
    dataIndex: "vehicleIdentity",
    key: "vehicleIdentity",
    sorter: (a, b) => a.vehicleIdentity.localeCompare(b.vehicleIdentity),
    sortDirections: ['descend', 'ascend'],
    width: 120
  },
  {
    title: "担当局",
    dataIndex: "bureau",
    key: "bureau",
    sorter: (a, b) => a.bureau.localeCompare(b.bureau),
    sortDirections: ['descend', 'ascend'],
    width: 150
  },
  {
    title: "当担段",
    dataIndex: "section",
    key: "section",
    sorter: (a, b) => a.section.localeCompare(b.section),
    sortDirections: ['descend', 'ascend'],
    width: 150
  },
  {
    title: '客车备注',
    dataIndex: 'vehicleDesc',
    key: 'vehicleDesc',
    ellipsis: true,              // 文本过长时显示省略号
    width: 100
  },
  {
    title: '辆序',
    dataIndex: 'vehicleSeq',
    key: 'vehicleSeq',
    width: 80
  },
  {
    title: '总辆数',
    dataIndex: 'totalSequence',
    key: 'totalSequence',
    width: 80
  },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',              // 固定在右侧
    width: 400,
  },
])

// 🎯 组件挂载后自动执行搜索
onMounted(() => {
  searchData()
})

// 📈 响应式数据定义
const totalData = ref(300)        // 总数据条数
const dataSource = ref([])        // 表格数据源

// 🔍 搜索条件（响应式对象）
const searchKey = reactive({
  vehicleInfo: '',               // 车次信息搜索关键词
  vehicleDesc: '',               // 车辆备注搜索关键词
  currentPage: 1,                // 当前页码
  pageSize: 10,                  // 每页显示条数
})

// 📄 分页变化处理函数
const onPageChange = (currentPage, pageNumber) => {
  // 更新搜索条件中的分页信息
  searchKey.currentPage = currentPage;
  searchKey.pageSize = pageNumber;
  // 重新搜索数据
  searchData()
}

// 🆕 控制新增车辆弹窗的显示状态
const newVehicleModal = ref(false)

// 🔍 搜索数据的核心函数
const searchData = () => {
  // 发送 POST 请求到后端分页接口
  HTTP.post(
      '/railway-vehicle/page',
      {
        ...searchKey              // 展开搜索条件对象
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      },
  ).then((res) => {
    // 更新表格数据和总数
    dataSource.value = res.data.records
    totalData.value = res.data.total
  })
}

// ✏️ 编辑表单的引用
const editForm = ref()

// ✏️ 点击编辑按钮的处理函数
const updateVehicleClick = (record) => {
  updateVehicleModal.value = true  // 显示编辑弹窗
  // 等待 DOM 更新后，设置表单数据
  nextTick(() => {
    editForm.value.setVehicleInfo(record)
  })
}

// 🗑️ 删除确认处理函数
const deleteConfirm = (record) => {
  // 发送 DELETE 请求删除指定车辆
  HTTP.delete(
      '/railway-vehicle/' + record.id,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      },
  ).then(() => {
    // 删除成功后重新搜索数据
    searchData()
  })
}

// 🔍 执行检测任务
const execDetectionTask = (record) => {
  // 发送 POST 请求启动检测任务
  HTTP.post(
      `/detection-task/exec/${record.id}`,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      },
  )
}

// 🖼️ 图片预览相关的响应式数据
const updateVehicleModal = ref(false)      // 编辑弹窗显示状态
const previewVehicleVisible = ref(false)   // 预览弹窗显示状态
const previewVehicleImage = ref('')        // 预览图片的 URL
const previewDirection = ref(1)            // 当前预览的方位
const currentPreviewRecordId = ref(null)   // 当前预览的车辆记录 ID

// 🖼️ 获取预览图片的函数
const fetchPreviewImage = () => {
  if (!currentPreviewRecordId.value) return;
  
  // 发送 GET 请求获取指定方位的图片
  HTTP.get(
      `/railway-vehicle/${currentPreviewRecordId.value}/${previewDirection.value}/preview`,
      {
        responseType: 'blob'        // 指定响应类型为二进制数据
      },
  ).then((res) => {
    // 释放之前的图片 URL（避免内存泄漏）
    if (previewVehicleImage.value) {
      URL.revokeObjectURL(previewVehicleImage.value);
    }
    // 创建新的图片 URL
    previewVehicleImage.value = URL.createObjectURL(res);
  })
}

// 🖼️ 点击预览按钮的处理函数
const previewVehicle = (record) => {
  currentPreviewRecordId.value = record.id;
  previewDirection.value = 1;              // 默认选择第一个方位
  fetchPreviewImage();                     // 获取默认方位的图片
  previewVehicleVisible.value = true;      // 显示预览弹窗
}

// 🖼️ 预览方位切换处理函数
const handlePreviewDirectionChange = () => {
  fetchPreviewImage();                     // 切换方位时重新获取图片
}

// 🖼️ 预览弹窗关闭处理函数
const handlePreviewClose = () => {
  // 释放图片 URL，防止内存泄漏
  if (previewVehicleImage.value) {
    URL.revokeObjectURL(previewVehicleImage.value);
    previewVehicleImage.value = '';
  }
  currentPreviewRecordId.value = null;
}

// 📊 查看检测结果的处理函数
const viewResults = (record) => {
  // 使用路由跳转到检测结果页面
  router.push({
    path: '/detection-result/' + record.taskItem.taskId
  });
};
</script>

<template>
  <div style="width: 100%">
    <!-- 📊 主数据表格 -->
    <a-table :data-source="dataSource"
             :columns="columns"
             bordered
             row-key="id"
             :scroll="{ y: 'calc(100vh - 300px)' }"
             :expand-column-width="85"
             :pagination="false">
      <!-- 📋 表格标题栏 -->
      <template #title>
        <div style="display: flex; justify-content: space-between">
          <span style="font-size: 20px; font-weight: bold">TVDS行车入站信息</span>
          <div style="display: flex; flex-wrap: nowrap; align-items: center">
            <!-- ➕ 新增按钮 -->
            <a-button :icon="h(PlusOutlined)" @click="newVehicleModal = true">客车入站</a-button>
            <!-- 🔍 搜索输入框 -->
            <a-input v-model:value="searchKey.vehicleInfo" placeholder="行车信息" allow-clear>
              <template #suffix>
                <a-tooltip title="行车信息精准搜索">
                  <info-circle-outlined style="color: rgba(0, 0, 0, 0.45)"/>
                </a-tooltip>
              </template>
            </a-input>
            <a-input v-model:value="searchKey.vehicleDesc" placeholder="行车备注" allow-clear>
              <template #suffix>
                <a-tooltip title="行车备注模糊搜索">
                  <info-circle-outlined style="color: rgba(0, 0, 0, 0.45)"/>
                </a-tooltip>
              </template>
            </a-input>
            <!-- 🔍 搜索按钮 -->
            <a-button type="primary" :icon="h(SearchOutlined)" @click="searchData">搜索</a-button>
          </div>
        </div>
      </template>
      
      <!-- 🎯 自定义操作列内容 -->
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <div style="display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: center; align-items: center;">
            <!-- 🖼️ 预览按钮 -->
            <a-button @click="previewVehicle(record)" style="margin-right: 5px">行车预览</a-button>
            
            <!-- 🔍 检测相关按钮（根据任务状态动态显示） -->
            <a-button style="margin-right: 5px" v-if="record.taskItem === null" @click="execDetectionTask(record)">开始检测</a-button>
            <div v-else>
              <a-button style="margin-right: 5px" @click="execDetectionTask(record)">再次检测</a-button>
              <a-button style="margin-right: 5px" v-if="record.taskItem.taskStatus === 1" type="primary" loading>进行中</a-button>
              <a-button style="margin-right: 5px" v-else-if="record.taskItem.taskStatus === 2" type="primary" @click="viewResults(record)">查看结果</a-button>
              <a-button style="margin-right: 5px" v-else-if="record.taskItem.taskStatus === 3" type="primary" danger>检测失败</a-button>
            </div>
          </div>
        </template>
      </template>
    </a-table>
  </div>
  
  <!-- 📄 分页组件 -->
  <div style="text-align: center; width: 100%; margin-top: 15px">
    <a-pagination show-quick-jumper :total="totalData" @change="onPageChange"/>
  </div>
  
  <!-- 🖼️ 行车大图预览弹窗 -->
  <a-modal v-model:open="previewVehicleVisible"
           title="行车大图预览"
           :footer="null"
           width="70%"
           :mask-closable="false"
           destroy-on-close
           @after-close="handlePreviewClose">
    <!-- 📐 方位选择器 -->
    <div style="text-align: center; margin-bottom: 16px;">
      <a-radio-group v-model:value="previewDirection" @change="handlePreviewDirectionChange" button-style="solid">
        <a-radio-button :value="0">方位1</a-radio-button>
        <a-radio-button :value="1">方位2</a-radio-button>
        <a-radio-button :value="2">方位3</a-radio-button>
        <a-radio-button :value="3">方位4</a-radio-button>
        <a-radio-button :value="4">方位5</a-radio-button>
      </a-radio-group>
    </div>
    <!-- 🖼️ 图片显示区域 -->
    <div style="overflow-x: auto">
      <img alt="行车大图"
           :src="previewVehicleImage"
           style="height: 70vh; display: block; margin: auto; border: 1px solid #eee;"/>
    </div>
  </a-modal>
  
  <!-- ✏️ 编辑行车信息弹窗 -->
  <a-modal v-model:open="updateVehicleModal"
           :mask-closable="false"
           :footer="null"
           title="修改行车信息">
    <VehicleInfoForm @after-submit="searchData" @close-modal="() => updateVehicleModal = false"
                     operation-type="edit" ref="editForm"/>
  </a-modal>
  
  <!-- 🆕 新建行车信息弹窗 -->
  <a-modal v-model:open="newVehicleModal"
           :mask-closable="false"
           :footer="null"
           style="top: 10px"
           destroy-on-close title="新增行车信息">
    <VehicleInfoForm @after-submit="searchData" @close-modal="() => newVehicleModal = false" operation-type="add"/>
  </a-modal>
</template>

<style scoped>
/* 🎨 组件样式（作用域限定） */
</style>