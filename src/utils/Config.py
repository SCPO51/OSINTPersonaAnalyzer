import yaml

class Config:
    _instance = None
    _initialized = False

    def __new__(cls, config_path="./src/config/config.yaml"):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            with open(config_path) as f:
                config = yaml.safe_load(f)
                cls._instance.base_models = config["base_models"]
                cls._instance.reasoning_models = config["reasoning_models"]
            cls._instance.base_index = 0
            cls._instance.reasoning_index = 0
        return cls._instance

    def get_base_model(self):
        model = self.base_models[self.base_index % len(self.base_models)]
        self.base_index += 1
        return model
    
    def get_reasoning_model(self):
        model = self.reasoning_models[self.reasoning_index % len(self.reasoning_models)]
        self.reasoning_index += 1
        return model

if __name__=="__main__":
    config1 = Config()
    config2 = Config()

    print(config1 is config2)  # 输出 True
    print(config1.get_base_model())
    print(config2.get_base_model())  # 会连续获取下一个模型
    print(config2.get_base_model())