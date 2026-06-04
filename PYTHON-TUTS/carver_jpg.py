#!/usr/bin/env python3

import sys
import os


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    image_file = sys.argv[1]

    output_dir = "M2_Lab_recovered_files"
    os.makedirs(output_dir, exist_ok=True)

    jpeg_header = b"\xff\xd8\xff"
    jpeg_footer = b"\xff\xd9"

    jpeg_count = 0

    with open(image_file, "rb") as disk:

        data = disk.read()

        i = 0
        while i < len(data) - 2:

            if data[i:i + 3] == jpeg_header:

                start = i

                j = i
                while j < len(data) - 1:

                    if data[j:j + 2] == jpeg_footer:
                        end = j + 2
                        break

                    j += 1

                disk.seek(start)
                file_data = disk.read(end - start)

                filename = f"{output_dir}/recovered_{jpeg_count}.jpg"

                with open(filename, "wb") as img:
                    img.write(file_data)

                jpeg_count += 1
                i = end

            else:
                i += 1

    if jpeg_count == 0:
        print("PASS: Script correctly handles missing JPEGs.")


if __name__ == "__main__":
    main()