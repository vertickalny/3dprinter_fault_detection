import os
import cv2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

# Настройка конфигурации модели
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("./configs/mask_rcnn_X_101_32x8d_FPN_3x.yaml")) # Нужно подредактировать путь к config file
cfg.MODEL.WEIGHTS = "./data/models/model_final.pth"
cfg.MODEL.DEVICE = "cpu"  # Используем CPU
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Порог уверенности
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1

# Регистрация собственного метадата с классом 'fail'
MetadataCatalog.get("custom_metadata").set(thing_classes=["fail"])

# Создание предиктора
predictor = DefaultPredictor(cfg)

# Папка с тестовыми изображениями
test_images_folder = "./data/samples/tests/"
output_folder = "./data/samples/output/" # Поменять на путь вывода
os.makedirs(output_folder, exist_ok=True)

# Обработка изображений
for image_filename in os.listdir(test_images_folder):
    image_path = os.path.join(test_images_folder, image_filename)
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Не удалось загрузить {image_path}, пропускаем...")
        continue

    # Инференс
    outputs = predictor(image)

    # Визуализация
    v = Visualizer(image[:, :, ::-1],
                   metadata=MetadataCatalog.get("custom_metadata"),
                   scale=0.5)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    
    # Сохранение результата
    output_path = os.path.join(output_folder, f"output_{image_filename}")
    cv2.imwrite(output_path, out.get_image()[:, :, ::-1])
    print(f"Сохранено: {output_path}")
