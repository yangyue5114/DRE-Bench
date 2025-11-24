## Questionnaire Instruction

Your task is to complete a questionnaire consisting of 400 questions. Each question is an abstract reasoning task. To solve each question, you can follow the steps below:

- Reason out the transformation rule by analyzing the three training sample pairs, namely how the input grids are converted into corresponding output grids.

- Apply the transformation rule to the test input grid and generate the correct test output grid.
For convenience, the test output grid has been pre-initialized with the content of the test input grid, so you can directly perform the rule-based transformation.

### Quick Start

1. **This project is an HTML application built with Flask. First, you need to install the necessary libraries to run it.**

```shell
pip install flask
```

2. **Run it in your terminal**
```shell
cd ./DRE-Bench/human_test/
python human.py
```

The port is open by default at 5000. You can also modify some parameters in `app.run()` in `human.py`.

3. **data**

We have already prepared the initial data, which is located in `./data/human_test_samples.json`. Of course, you can also click **Select File** to upload your own data; the JSON data uploaded via file will be saved in `./uploads/`. Alternatively, you can use a **relative path** to read it, for example, by entering `data/human_test.json` in the input box.

After reading the data, the entire JSON object will be stored in `metaData` in **memory**. When you click `Next`, the data you entered will be automatically updated in `metaData`. It will only be saved locally when you click `Submit`. **In other words, remember to click the `Submit` button before closing your browser session.** 😊

Submitted data is stored in `./submissions/`, in the format `submission_int(time.time()).json`. When you want to continue the process the next time you open the site, you can simply load the data from here. 😎

- Good luck! 🤠
