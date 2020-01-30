import getFrames as gf
import glob
import frametotext as ftt

if __name__ == '__main__':
    videopath = glob.glob('../videos_convertidos/ch0019_00000001575014401.mp4')
    gf.get_video_frames(videopath[0], 8)
    ftt.get_video_begin_end(videopath[0], 8)