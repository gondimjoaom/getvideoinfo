import getFrames as gf
import frametotext as ftt

if __name__ == '__main__':
    gf.get_video_frames('../videos_convertidos/ch0019_00000001575014401.mp4', 8)
    ftt.get_video_begin_end('../videos_convertidos/ch0019_00000001575014401.mp4', 8)