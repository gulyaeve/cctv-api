import subprocess
import sys
import requests
from config import settings

requested_camera = sys.argv[1]
print(requested_camera)
requested_camera = requested_camera.split("/")[0]

camera_request = requests.get(
    f"{settings.CAMERAS_API}/{requested_camera.split("_")[0]}",
    verify=False,
    headers={"Authorization": f"Bearer {settings.TOKEN_BEARER}"}
)

def main():
    camera_data = camera_request.json()

    # Источник (RTSP камера)
    if requested_camera.endswith("_p"):
        source_rtsp = camera_data["rtsp_url_preview"]
    else:
        source_rtsp = camera_data["rtsp_url"]
    # print(source_rtsp)

    # Куда отправляем (RTSP сервер)
    # Используем localhost, если MediaMTX запущен на той же машине
    output_rtsp = f"{settings.media_server_rtsp_base_url}/{requested_camera}"

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"]

    cmd.extend(["-rtsp_transport", f"{settings.RTSP_TRANSPORT}"])
    # cmd.extend([
    #     "-fflags", "nobuffer",
    #     "-flags", "low_delay",
    #     "-probesize", "32",
    #     "-analyzeduration", "0",
    #     "-rtsp_transport", f"{settings.RTSP_TRANSPORT}"
    # ])

    cmd.extend(
        [
            "-i", source_rtsp,
            "-c", "copy",
            "-f", "rtsp",
            f"{output_rtsp}?jwt={settings.TOKEN_BEARER}",
            # "-rtsp_transport", "udp"
        ]
    )

    print(cmd)
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
