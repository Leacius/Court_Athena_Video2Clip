import cv2
import pandas as pd
from pathlib import Path

class Label:
    def __init__(self, json_path):
        self.df = pd.read_json(json_path)
        self.df_Action = self.__get_EventType()
        self.df_Serve = self.__get_Serve()
        self.df_win_point = self.__get_win_point()
        self.df_serveNaction = self.__get_serveNaction()

        self.name = str(json_path).split("\\")[-1].split(".")[0] 
    
    def __get_Serve(self):
        idx = (self.df.eventType == "發球").tolist() 
        df = self.df.iloc[idx]

        return df

    def __get_EventType(self):
        idx = (self.df.eventType == "動作").tolist() 
        df = self.df.iloc[idx]

        return df
    
    def __get_win_point(self):
        idx = (self.df.eventType == "贏局").tolist()
        df = self.df.iloc[idx]

        return df

    def __get_serveNaction(self):
        idx_s = (self.df.eventType == "發球").tolist()
        idx_a = (self.df.eventType == "動作").tolist()
        idx = [idx_s[i] or idx_a[i] for i in range(len(idx_s))]
        df = self.df.iloc[idx]

        return df

    def extract_list(self, df, ActionType):
        
        if ActionType == 'actions':
            action_list = []
            player_list = [df.labels.iloc[i][-2]['value'] for i in range(len(df))]
            for x in df.labels:
                name = ""
                for i in range(2):
                    name += x[i]['value']
                action_list.append(name)

            return df.startFrame, df.duration, action_list, player_list, df.eventType

        elif ActionType == 'serves':
            serve_list = []
            player_list = [df.labels.iloc[i][-1]['value'] for i in range(len(df))]

            for x in df.labels:
                name = x[0]["value"] + x[3]['value']
                serve_list.append(name)
            
            return df.startFrame, df.duration, serve_list, player_list, df.eventType
            
        elif ActionType == 'both':
            player_list = []
            events_list = []
            for i in range(len(df)):
                if df.iloc[i].eventType == '動作':
                    player_list.append(df.iloc[i].labels[-2]['value'])
                    name = df.iloc[i].labels[0]["value"] + "_" + df.iloc[i].labels[1]["value"]
                    events_list.append(name)
                        
                elif df.iloc[i].eventType == '發球':
                    player_list.append(df.iloc[i].labels[-1]['value'])
                    name = df.iloc[i].labels[0]["value"] + "_" + df.iloc[i].labels[3]["value"] # ToDo: fine-grained
                    events_list.append(name)

            return df.startFrame, df.duration, events_list, player_list, df.eventType,
    
    def get_Action_Name(self, ActionType):
        '''
        AntionType : serves / actions / both
        '''
        startFrame_list = []
        duration_list = []
        action_list = []
        player_list = []
        if (ActionType == 'actions'):
            startFrame_list, duration_list, action_list, player_list, EventType = self.extract_list(self.df_Action, ActionType)
        
        elif (ActionType == 'serves'):
            startFrame_list, duration_list, action_list, player_list, EventType = self.extract_list(self.df_Serve, ActionType)

        elif (ActionType == 'both'):
            startFrame_list, duration_list, action_list, player_list, EventType = self.extract_list(self.df_serveNaction, ActionType)

        dictionary = {'StartFrame':startFrame_list, 'Duration':duration_list, 'Actions':action_list, 'Player':player_list, 'EventType':EventType}
        df = pd.DataFrame(dictionary).reset_index(drop=False)
        
        return df
