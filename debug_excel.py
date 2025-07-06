import pandas as pd
import os

def debug_excel_structure(file_path):
    """
    调试Excel文件结构，查看实际的列名和数据格式
    """
    print(f"正在分析文件: {file_path}")
    print("=" * 50)
    
    try:
        # 读取Excel文件的所有工作表
        excel_file = pd.ExcelFile(file_path)
        print(f"工作表数量: {len(excel_file.sheet_names)}")
        print(f"工作表名称: {excel_file.sheet_names}")
        print()
        
        for i, sheet_name in enumerate(excel_file.sheet_names):
            print(f"工作表 {i+1}: {sheet_name}")
            print("-" * 30)
            
            # 读取工作表数据
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"数据行数: {len(df)}")
            print(f"数据列数: {len(df.columns)}")
            print(f"列名: {list(df.columns)}")
            print()
            
            # 显示前几行数据
            print("前5行数据:")
            print(df.head())
            print()
            
            # 查找可能的车辆编号列
            possible_vehicle_cols = []
            possible_seq_cols = []
            
            for col in df.columns:
                col_str = str(col).lower()
                if any(keyword in col_str for keyword in ['车号', '车辆', 'vehicle', '编号']):
                    possible_vehicle_cols.append(col)
                if any(keyword in col_str for keyword in ['辆序', '序号', '车厢', 'seq', '序']):
                    possible_seq_cols.append(col)
            
            if possible_vehicle_cols:
                print(f"可能的车辆编号列: {possible_vehicle_cols}")
            if possible_seq_cols:
                print(f"可能的车厢序号列: {possible_seq_cols}")
            
            print("=" * 50)
            print()
            
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")

# 测试您的Excel文件
file_path = r"d:\tvds-system\TV故障及全列图片\5.5-K1072\2025年05月05日10时21分27秒京九线北京西上行到达(固安)探测站K1072车次列车车辆信息及故障信息过车图片\2025年05月05日10时21分27秒京九线北京西上行到达(固安)探测站K1072车次列车车辆及故障信息.xls"

if os.path.exists(file_path):
    debug_excel_structure(file_path)
else:
    print(f"文件不存在: {file_path}")