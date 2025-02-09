import random

import numpy as np
import tritonclient.http as httpclient


TRITON_HTTP_URL = "localhost:5000"


def main():
    triton_http_client = httpclient.InferenceServerClient(url=TRITON_HTTP_URL)

    # Simplest: Image in, String out
    model_name = "image_in__string_out"

    input_image = np.random.randint(0, 256, (random.randint(512, 1024), random.randint(512, 1024), 3), dtype=np.uint8)
    input_image_batch = np.expand_dims(input_image, axis=0)

    inputs = [
        httpclient.InferInput("IMAGE", input_image_batch.shape, "UINT8"),
    ]
    inputs[0].set_data_from_numpy(input_image_batch)

    outputs = [
        httpclient.InferRequestedOutput("PREDICTED_CLASS")
    ]

    results = triton_http_client.infer(model_name=model_name, inputs=inputs, outputs=outputs)

    predicted_class = results.as_numpy("PREDICTED_CLASS")
    predicted_class = predicted_class[0].decode("utf-8")

    print(predicted_class)

if __name__ == "__main__":
    main()
