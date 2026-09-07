/**
 * Remotion High-Performance Configuration
 * Optimizes headless Chromium rendering on GitHub Actions & cloud runners:
 * 1. Uses swangle / swiftshader software OpenGL for maximum CPU rasterization throughput.
 * 2. Uses fast JPEG frame capture instead of CPU-heavy lossless PNG.
 * 3. Sets optimal Linux Chromium flags to eliminate shared memory bottlenecks.
 */

import { Config } from "@remotion/cli/config";

// OpenGL software renderer
Config.setChromiumOpenGlRenderer("swangle");

// Fast JPEG encoding for frame interchange between Chrome and FFmpeg (3x-5x faster than PNG)
Config.setVideoImageFormat("jpeg");
Config.setStillImageFormat("jpeg");
Config.setJpegQuality(85);

// Output configuration
Config.setPixelFormat("yuv420p");
Config.setCodec("h264");
Config.setOverwriteOutput(true);
Config.setChromiumDisableWebSecurity(true);

// Linux / CI memory and multi-process optimization
Config.setChromiumMultiProcessOnLinux(true);
