#  The MIT License (MIT)
#  Copyright © 2023 Yuma Rao
#  Copyright © 2024 WOMBO
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the “Software”), to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import base64
from io import BytesIO

from PIL import Image


WATERMARK = Image.open("w_watermark.png")


def watermark_image(image: Image.Image) -> Image.Image:
    image_copy = image.copy()
    wm = WATERMARK.resize((image_copy.size[0], int(image_copy.size[0] * WATERMARK.size[1] / WATERMARK.size[0])))
    wm, alpha = wm.convert("RGB"), wm.split()[3]
    image_copy.paste(wm, (0, image_copy.size[1] - wm.size[1]), alpha)
    return image_copy


def add_watermarks(images: list[Image.Image]) -> list[bytes]:
    """
    Add watermarks to the images.
    """

    def save_image(image: Image.Image) -> bytes:
        image = watermark_image(image)
        with BytesIO() as image_bytes:
            image.save(image_bytes, format="JPEG")
            return base64.b64encode(image_bytes.getvalue())

    return [save_image(image) for image in images]
