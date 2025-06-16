"""Deals with fetching texts from database."""

import os
import sqlite3


def database_file_absolute_path():
    """Get full path of directory where source files are stored.

    This is required for later fetching entry from data.db which is
    stored in same directory as app.

    Returns:
        str: The path of directory of source file.
    """
    database_filename = "data.db"
    database_directory_absolute_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        database_directory_absolute_path,
        database_filename,
    )


def init_database():
    """Initialize database with required tables if they don't exist."""
    database_file = database_file_absolute_path()
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # 创建中文文本表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zh_data (
            id INTEGER PRIMARY KEY,
            txt TEXT NOT NULL,
            difficulty INTEGER NOT NULL
        )
    """)
    
    # 如果中文表为空，添加一些示例中文文本
    cursor.execute("SELECT COUNT(*) FROM zh_data")
    if cursor.fetchone()[0] == 0:
        sample_texts = [
            (1, "这是一个简单的打字测试。", 1),
            (2, "练习打字可以提高你的输入速度。", 1),
            (3, "中文打字需要掌握拼音输入法。", 1),
            (4, "打字速度的提升需要持之以恒的练习。", 2),
            (5, "正确的打字姿势可以提高打字效率。", 2),
            (6, "打字时要注意手指的位置和移动方式。", 2),
            (7, "熟练的打字技能在现代社会非常重要。", 3),
            (8, "打字速度的提升可以大大提高工作效率。", 3),
            (9, "练习打字时要保持专注和耐心。", 3),
            (10, "打字测试可以帮助你了解自己的打字水平。", 4),
            (11, "通过不断的练习，你的打字速度会逐渐提高。", 4),
            (12, "打字时要注意准确性和速度的平衡。", 4),
            (13, "良好的打字习惯可以让你受益终身。", 5),
            (14, "打字技能的提升需要系统的训练和指导。", 5),
            (15, "坚持练习是提高打字速度的关键。", 5),
        ]
        cursor.executemany("INSERT INTO zh_data (id, txt, difficulty) VALUES (?, ?, ?)", sample_texts)
        connection.commit()

    connection.close()


def fetch_text_from_id(serial_id, language="en"):
    """Fetch row from database.

    Args:
        serial_id (int): The unique ID of database entry.
        language (str): Language of the text to fetch ("en" or "zh").

    Returns:
        str: The text corresponding to the entry_id.
    """
    # 确保数据库已初始化
    init_database()
    
    database_file = database_file_absolute_path()
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # 根据语言选择表
    table_name = "zh_data" if language == "zh" else "data"
    
    # 获取文本
    cursor.execute(f"SELECT txt FROM {table_name} where id=?", (serial_id,))
    result = cursor.fetchone()
    
    if result is None:
        # 如果找不到指定ID的文本，返回一个默认文本
        if language == "zh":
            return "这是一个默认的中文打字测试文本。"
        else:
            cursor.execute("SELECT txt FROM data where id=1")
            result = cursor.fetchone()
    
    text = result[0]
    connection.close()

    return text
