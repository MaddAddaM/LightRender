import os, subprocess, math, glob
from LightPosition import LightPosition
from constants import CARTESIAN_COORDS as COORDS
from PIL import Image

FPS = 20
RESOURCES_PATH = "Resources"
FRAMES_TEMP_PATH = "%s/Frames" % RESOURCES_PATH
VIDEO_SOURCE_FILE = "video.mp4"
RENDER_OUTPUT_FILE = "video.bin"

# Lights are on a fixed grid, so we can compute their theoretical positions
# NOTE: ROWS is numbered from bottom to top, but PIL starts in the top left.
LIGHT_POSITIONS = [LightPosition(c*50+25, 1000-(r*50+25)) for c, r in COORDS]

# Cleanup at start, so I can leave my temp files at the end for debugging
print("Clearing frames temp folder")
for tempFilePath in glob.glob("%s/*" % FRAMES_TEMP_PATH):
	if os.path.isfile(tempFilePath):
		os.unlink(tempFilePath)

# Query the video properties I need to know
print("Getting video duration")
cmd = [
	"ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", 
	"default=noprint_wrappers=1:nokey=1", "%s/%s" % (RESOURCES_PATH, VIDEO_SOURCE_FILE)]
ffProbeSubprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE)
ffProbeOutput, ffProbeError = ffProbeSubprocess.communicate()
videoDuration = float(ffProbeOutput)
print("Video duration is %fs" % videoDuration)

cmd = [
	"ffprobe", "-v", "error", "-show_entries", "stream=width", "-of", 
	"default=noprint_wrappers=1:nokey=1", "%s/%s" % (RESOURCES_PATH, VIDEO_SOURCE_FILE)]
ffProbeSubprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE)
ffProbeOutput, ffProbeError = ffProbeSubprocess.communicate()
videoWidth = int(ffProbeOutput)
print("Video width is %dpx" % videoWidth)

cmd = [
	"ffprobe", "-v", "error", "-show_entries", "stream=height", "-of", 
	"default=noprint_wrappers=1:nokey=1", "%s/%s" % (RESOURCES_PATH, VIDEO_SOURCE_FILE)]
ffProbeSubprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE)
ffProbeOutput, ffProbeError = ffProbeSubprocess.communicate()
videoHeight = int(ffProbeOutput)
print("Video height is %dpx" % videoHeight)

# Extract image files to represent each frame in my rendering
print("Extracting frame images")
cmd = [
	"ffmpeg", "-i", "%s/%s" % (RESOURCES_PATH, VIDEO_SOURCE_FILE), "-vf", "fps=%d" % FPS, 
	"%s/frame%%06d.png" % FRAMES_TEMP_PATH]
ffMpegSubprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE)
ffMpegOutput, ffMpegError = ffMpegSubprocess.communicate()
print("Frame images extracted")

# Extract color for each light from my images
numberOfFrameImages = int(math.floor((videoDuration * FPS)))
print("Extracting pixel data from %d frame images" % numberOfFrameImages)

lightRenderData = []

for frameNumber in xrange(1, numberOfFrameImages + 1):
	frameImage = Image.open("%s/frame%06d.png" % (FRAMES_TEMP_PATH, frameNumber))
	framePixels = frameImage.load()

	for lightIndex, lightPosition in enumerate(LIGHT_POSITIONS, 1):
		lightPixel = framePixels[
			lightPosition.GetRelativeX(videoWidth), lightPosition.GetRelativeY(videoHeight)]

		lightR = int(lightPixel[0])
		lightG = int(lightPixel[1])
		lightB = int(lightPixel[2])

		if __debug__:
			print(
				"Frame %d/%d, Light %d/%d is (%d, %d, %d)" % (
					frameNumber, numberOfFrameImages, lightIndex,
					len(LIGHT_POSITIONS), lightR, lightG, lightB))

		lightRenderData.append(lightR)
		lightRenderData.append(lightG)
		lightRenderData.append(lightB)

print("Generated render binary of %d bytes" % len(lightRenderData))

# Output the rendering to a file
print("Storing to binary stream file")
with open("%s/%s" % (RESOURCES_PATH, RENDER_OUTPUT_FILE), "wb") as outputFile:
	outputFile.write(bytearray(lightRenderData))
print("Stored rendering to %s" % RENDER_OUTPUT_FILE)

# vim: set ts=8 sw=8 noet:
