from hllama import json_utils


class TestJSONUtils:
    def test_match_structure1(self):
        A = {"key1": str, "key2": {"key3": str, "key4": int, "key5": list}}
        B = {"key1": "hello", "key2": {"key3": "world", "key4": 100, "key5": [1, 2, 3]}}

        result = json_utils.match_structure(A, B)
        assert result is True

    def test_match_structure2(self):
        A = {"key1": str, "key2": [{"key3": str, "key4": list}]}
        B = {
            "key1": "example",
            "key2": [
                {"key3": "data", "key4": [1, 2, 3]},
                {"key3": "more data", "key4": [4, 5]},
            ],
        }

        result = json_utils.match_structure(A, B)
        assert result is True

    def test_parse_first_json_snippet(self):
        raw_string = """
Here's a JSON object with instruction-response pairs that adhere to your requirements. The instructions are based on the relationships and attributes of the entities involved, while ensuring they remain general and relevant to broader use cases:
"""
        assert json_utils.parse_first_json_snippet(raw_string) is None

        raw_string = """
Here's a JSON object with instruction-response pairs that adhere to your requirements. The instructions are based on the relationships and attributes of the entities involved, while ensuring they remain general and relevant to broader use cases:

{
  "contents": [
    {
      "instruction": "how to check the system specifications on a 2023 MacBook M1 Pro",
      "response": "To check the system specifications on a 2023 MacBook M1 Pro, click on the Apple logo at the top left corner of the screen, select 'About This Mac' from the drop-down menu. This will open a window displaying information such as the macOS version, processor type, memory, and other hardware details."
    },
    {
      "instruction": "how to set up development environment on a MacBook with M1 Pro chip",
      "response": "To set up a development environment on a MacBook with an M1 Pro chip, first ensure that you have installed Xcode from the App Store. Next, install Homebrew by opening the Terminal and running the installation command from the Homebrew website. You can then use Homebrew to install additional tools like Git, Node.js, and Python. Finally, configure your IDE of choice, such as Visual Studio Code, to work with these tools."
    },
    {
      "instruction": "how to optimize battery life while coding on a MacBook M1 Pro",
      "response": "To optimize battery life while coding on a MacBook M1 Pro, adjust the screen brightness to a lower setting, close unnecessary apps and tabs, and switch the Energy Saver settings to 'Low Power Mode'. Additionally, consider using more efficient programming tools and practices that consume less CPU and memory resources."
    },
    {
      "instruction": "how to troubleshoot software compilation errors in Xcode on a new MacBook",
      "response": "To troubleshoot software compilation errors in Xcode on a new MacBook, first ensure that Xcode is fully updated via the App Store. Check the error messages for clues—common issues might involve missing libraries or frameworks. Review your project's build settings, ensure all dependencies are correctly configured, and clean the build folder by going to Product > Clean Build Folder in Xcode."
    },
    {
      "instruction": "how to use terminal commands to manage applications on a MacBook M1 Pro",
      "response": "To manage applications on a MacBook M1 Pro using terminal commands, open the Terminal app. You can install applications using Homebrew by typing 'brew install [application-name]'. To uninstall, use 'brew uninstall [application-name]'. You can also update all your Homebrew-managed applications by typing 'brew update' followed by 'brew upgrade'."
    }
  ]
}
"""

        result = json_utils.parse_first_json_snippet(raw_string)
        assert isinstance(result, dict)
