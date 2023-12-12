import os
from FastSAM.fastsam import FastSAM, FastSAMPrompt

class FSAM:
    def __init__(self):
        self.DIR_PATH = os.path.dirname(os.path.realpath(__file__))
        self.model = FastSAM(f'{self.DIR_PATH}/FastSAM/weights/FastSAM_x.pt')
        self.DEVICE = 'cpu'

    def execute_fsam(self, image_path, points):
        everything_results = self.model(image_path, device=self.DEVICE, retina_masks=True, imgsz=1024, conf=0.4, iou=0.9,)
        prompt_process = FastSAMPrompt(image_path, everything_results, device=self.DEVICE)
        ann = prompt_process.point_prompt(points=points, pointlabel=[1])
