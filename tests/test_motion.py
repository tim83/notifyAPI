from pathlib import Path

import pytest

import notifyAPI.motion


def test_get_most_recent_movie(tmp_path: Path):
    notifyAPI.motion.MOTION_MEDIA_LOCATION = tmp_path

    with pytest.raises(FileNotFoundError):
        notifyAPI.motion.get_most_recent_movie()

    filelist = [
        tmp_path / "2012-10-02/12-03-23.mp4",
        tmp_path / "2013-12-12/15-03-23.mp4",
        tmp_path / "2022-10-02/12-03-23.jpg",
        tmp_path / "2013-12-03/12-03-23.mp4",
    ]
    for file in filelist:
        file.parent.mkdir(parents=True)
        file.touch()

    most_recent_file = notifyAPI.motion.get_most_recent_movie()
    assert most_recent_file == tmp_path / "2013-12-12/15-03-23.mp4"
