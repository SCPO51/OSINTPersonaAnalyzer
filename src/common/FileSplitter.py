import os


class FileSplitter:
    @staticmethod
    def split_large_file(input_file, output_prefix, max_size_kb=128):
        """
        分割大文件为多个不超过指定大小的小文件

        参数:
            input_file: 输入文件路径
            output_prefix: 输出文件前缀（如: "output" 会生成 "output_part1.ext"）
            max_size_kb: 最大分块大小（单位KB，默认为128KB）

        返回:
            生成的分块文件路径列表

        异常:
            ValueError: 当遇到单行内容超过最大限制时抛出
        """
        file_extension = os.path.splitext(input_file)[1]  # 保持原文件扩展名
        max_size = max_size_kb * 1024  # 转换为字节
        part_number = 1
        current_lines = []
        current_size = 0
        part_files = []

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                for line in f:
                    line_size = len(line.encode("utf-8"))

                    # 验证单行大小
                    if line_size > max_size:
                        raise ValueError(
                            f"单行大小 {line_size} 字节超过限制 {max_size} 字节"
                        )

                    # 检查是否需要创建新分块
                    if current_size + line_size > max_size:
                        FileSplitter.write_chunk(
                            output_prefix,
                            file_extension,
                            part_number,
                            current_lines,
                            part_files,
                        )
                        part_number += 1
                        current_lines = [line]
                        current_size = line_size
                    else:
                        current_lines.append(line)
                        current_size += line_size

                # 写入最后剩余的内容
                if current_lines:
                    FileSplitter.write_chunk(
                        output_prefix,
                        file_extension,
                        part_number,
                        current_lines,
                        part_files,
                    )
        except FileNotFoundError:
            raise FileNotFoundError(f"输入文件 {input_file} 不存在")

        return part_files

    @staticmethod
    def write_chunk(prefix, extension, part_num, lines, part_list):
        """将当前缓冲区写入分块文件"""
        chunk_path = f"{prefix}_part{part_num}{extension}"
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        part_list.append(chunk_path)
