from tqdm import tqdm
from pathlib import Path
from myutils import *

class Clips:
    def __init__(self, args) -> None:

        # Path
        self.videos_path = list(Path(args.video_path).glob("*.mp4"))
        self.label_files = list(Path(args.json_path).glob("*.json"))
        self.clips_path = args.save_root + "clips/"

    def vid2clip(self, cap, df, save_folder):
        Path(save_folder[0]).mkdir(parents=True, exist_ok=True)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        for i in tqdm(range(len(df))):
            start = df.StartFrame.iloc[i]
            length = df.Duration.iloc[i]
            labels = df.EventType.iloc[i]

            # video to clip
            out = cv2.VideoWriter(f"./{save_folder[0]}/{i}_{labels}.avi", cv2.VideoWriter_fourcc(*'MJPG'), 15, (w,h))

            cap.set(1, start)
            for _ in tqdm(range(length), leave=False):
                success, frame = cap.read()

                if not success:
                    break

                out.write(frame)
            out.release()

    def Run(self, eventType = "both", save_folder = ["clips"]):
        for vid, lab in zip(self.videos_path, self.label_files):
            vid = str(vid)
            lab = str(lab)
            lab = Label(lab)
            df_serveNaction = lab.get_Action_Name(eventType)

            # run video
            cap = cv2.VideoCapture(vid)
            self.vid2clip(cap, df_serveNaction, save_folder)
            cap.release()