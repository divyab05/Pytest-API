printv2_body = {
    "comment": "This is the schema for the microservice PRINT end point",
    "jobId": "test_single_8x11_mac",
    "type": "printv2",
    "payload": [
        {
            "data": "https://prv-labels-cls.gcs.pitneycloud.com/usps/517575957/outbound/label/93e5383bd3e04764b3b59aa2d6c6c068.pdf",
            "documentType": "pdf",
            "dataType": "url",
            "formName": "8x11",
            "printType": "SHEET",
            "offset": {
                "right": 0,
                "top": 0
            },
            "orientation": "PORTRAIT",
            "printerName": "HP LaserJet M207-M212",
            "name": "test_single_4x6_mac"
        }

    ],
    "deviceInfo": [
        {
            "serialNumber": "AP-DP1LZH3-DP1LZH3-qa",
            "printerName": [
                "TIFF Image Printer 12"
            ]
        }
    ],
    "serialNumber": "IN-NI009GA-MLT-C02DT3Z0MD6N-qa",
    "subscriptionId": "SENDPROANYWHERE"
}
