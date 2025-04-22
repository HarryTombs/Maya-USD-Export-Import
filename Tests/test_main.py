import pytest
from main import CreateUSDA

def test_createUSDA():
    with patch("maya.cmds") as mock_cmds:
        mock_cmds.file.return_value = "/Path/To/Scene"

        result = CreateUSDA()

        mock_cmds.file.assert_called_once_with(scene_path = "/Path/To/Scene")
        assert result == "/Path/To/Scene"