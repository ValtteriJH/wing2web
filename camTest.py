from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

imgs = ['testPics/add-text-to-photos-app01.jpg', 'testPics/fusariTest.jpg']

for img_path in imgs:
    result, elapse = engine(img_path)
    print(result)
    print(elapse)
