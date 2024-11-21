from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import numpy as np
from semi1 import RGBto_YUV, YUVto_RGB, resize_image, compress_to_bw, encoding, DCT, DWT
from typing import Union

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
            

@app.get("/api/convert_rgb_to_yuv")
def convert_rgb_to_yuv(R: int, G: int, B: int):
    converter = RGBto_YUV()
    Y, U, V = converter.RGB_to_YUV(R, G, B)
    return {"Y": Y, "U": U, "V": V}

        
@app.get("/api/convert_yuv_to_rgb")
def convert_rgb_to_yuv(Y: int, U: int, V: int):
    converter = YUVto_RGB()
    R, G, B = converter.YUV_to_RGB(Y, U, V)
    return {"R": R, "G": G, "B": B}



# Resize image endpoint (with query params for width, height, and quality)
@app.get("/api/resize_image")
def resize_image_endpoint(input_image: str = Query(...), output_image: str = Query(...),
                           width: int = Query(...), height: int = Query(...),
                           quality: Optional[int] = Query(28)):
    """Resizes an image with specified width, height, and quality."""
    try:
        resize_image(input_image, output_image, width, height, quality)
        return {"message": f"Image resized and saved to {output_image}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Compress image to black and white endpoint (with query params for input and output paths)
@app.get("/api/compress_to_bw")
def compress_to_bw_endpoint(input_image_path: str = Query(...), output_image_path: str = Query(...)):
    """Compresses image to black and white."""
    try:
        compress_to_bw(input_image_path, output_image_path)
        return {"message": f"Compressed and converted image saved at {output_image_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        
@app.post("/api/encoding")
def encoding_endpoint(byte_sequence: List[int]):
    byte_sequence = bytes(byte_sequence)  # Convert list to bytes
    encoded_result = encoding(byte_sequence)
    return {"encoded_result": list(encoded_result)}
    


# DCT encoding endpoint (with query params for the input block)
@app.get("/api/encode_dct")
def encode_dct_endpoint(
    row1_0: int = Query(...), row1_1: int = Query(...), row1_2: int = Query(...),
    row2_0: int = Query(...), row2_1: int = Query(...), row2_2: int = Query(...),
    row3_0: int = Query(...), row3_1: int = Query(...), row3_2: int = Query(...)
):
    """Encodes an input block using DCT, passed as individual query parameters."""
    try:
        # Build the 2D input block (List[List[int]]) from query params
        input_block = [
            [row1_0, row1_1, row1_2],
            [row2_0, row2_1, row2_2],
            [row3_0, row3_1, row3_2]
        ]
        dct_processor = DCT()
        dct_encoded = dct_processor.encode_dct(np.array(input_block))
        return {"dct_encoded": dct_encoded.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        


# DCT decoding endpoint (with query params for the encoded DCT block)
@app.get("/api/decode_dct")
def decode_dct_endpoint(
    row1_0: int = Query(...), row1_1: int = Query(...), row1_2: int = Query(...),
    row2_0: int = Query(...), row2_1: int = Query(...), row2_2: int = Query(...),
    row3_0: int = Query(...), row3_1: int = Query(...), row3_2: int = Query(...)
):
    """Decodes a DCT-encoded input block, passed as individual query parameters."""
    try:
        # Build the 2D input block (List[List[int]]) from query params
        input_block = [
            [row1_0, row1_1, row1_2],
            [row2_0, row2_1, row2_2],
            [row3_0, row3_1, row3_2]
        ]
        dct_processor = DCT()
        dct_decoded = dct_processor.decode_dct(np.array(input_block))
        return {"dct_decoded": dct_decoded.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DWT encoding endpoint (with query params for the input signal)
@app.get("/api/encode_dwt")
def encode_dwt_endpoint(input_signal: List[int]):
    wavelet_processor = DWT(wavelet='db2', mode='smooth')
    cA, cD = wavelet_processor.encode_dwt(input_signal)
    return {"approximation_coefficients": cA, "detail_coefficients": cD}



# DWT decoding endpoint (with query params for the input signal)
@app.get("/api/decode_dwt")
def decode_dwt_endpoint(input_signal: List[int] = Query(...)):
    """Decodes an input signal using DWT."""
    try:
        wavelet_processor = DWT(wavelet='db2', mode='smooth')
        decoded_signal = wavelet_processor.decode_dwt(input_signal)
        return {"decoded_signal": decoded_signal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example for more dynamic parameters (passing a matrix as query parameters)
@app.get("/api/encode_dynamic_matrix")
def encode_dynamic_matrix(
    row1: List[int] = Query(..., description="First row of the matrix"),
    row2: List[int] = Query(..., description="Second row of the matrix"),
    row3: List[int] = Query(..., description="Third row of the matrix")
):
    """Encodes an input matrix using dynamic query parameters."""
    try:
        # Build the 2D input block (List[List[int]]) from query params
        input_block = [row1, row2, row3]

        # Example processing (replace with your actual logic)
        processed_result = input_block  # Placeholder for processing logic
        return {"processed_matrix": processed_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example endpoint for testing various parameters dynamically
@app.get("/test_params")
def test_params(
    R: int = Query(255, alias="r", description="Red channel value (default: 255)"),
    G: int = Query(100, alias="g", description="Green channel value (default: 100)"),
    B: int = Query(50, alias="b", description="Blue channel value (default: 50)"),
    width: int = Query(640, alias="width", description="Width of the image (default: 640)"),
    height: int = Query(480, alias="height", description="Height of the image (default: 480)")
):
    """Test endpoint to show parameters in Swagger UI."""
    # Example RGB to YUV conversion
    yuv_converter = RGBto_YUV()
    Y, U, V = yuv_converter.RGB_to_YUV(R, G, B)
    return {
        "input_rgb": {"R": R, "G": G, "B": B},
        "converted_yuv": {"Y": Y, "U": U, "V": V},
        "resize_params": {"width": width, "height": height}
    }
