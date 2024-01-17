from pywhispercpp.model import Model

model = Model('<model_path>/ggml-base.en.bin', n_threads=6)
print(Model.system_info())  # and you should see COREML = 1