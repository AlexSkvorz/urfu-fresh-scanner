from dataclasses import dataclass

from ultralytics import YOLO

@dataclass
class FreshClassifierResult:
    is_rotten: bool
    name: str

class FreshClassifier:
    model = YOLO("../runs/classify/train4/weights/best.pt")
    CONFIDENCE_THRESHOLD = 0.6

    def predict(self, image_path: str) -> FreshClassifierResult | None:
        results = self.model.predict(image_path)
        probs = results[0].probs
        predicted_class_index = probs.top1
        predicted_class_confidence = probs.data[predicted_class_index].item()

        if predicted_class_confidence < self.CONFIDENCE_THRESHOLD:
            return None

        predicted_class_name = results[0].names[predicted_class_index]
        if 'rotten' in predicted_class_name:
            is_rotten = True
            predicted_class_name = predicted_class_name.replace('rotten', '')
        else:
            is_rotten = False
            predicted_class_name = predicted_class_name.replace('fresh', '')

        match predicted_class_name:
            case 'okra':
                product_name = "бамия"
            case 'tomato':
                product_name = "томат"
            case 'apples':
                product_name = "яблоко"
            case 'banana':
                product_name = "банан"
            case 'potato':
                product_name = "картофель"
            case 'orange':
                product_name = "апельсин"
            case 'bittergroud':
                product_name = "горький огурец"
            case 'cucumber':
                product_name = "огурец"
            case 'capsicum':
                product_name = "стручковый перец"
            case _:
                product_name = "неизвестный продукт"

        return FreshClassifierResult(
            is_rotten=is_rotten,
            name=product_name,
        )
