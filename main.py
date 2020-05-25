import os
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import txtimage

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    # using 16 accounts - Because of API Quota Limitation
    accounts = 16
    video_id = "1f2NLsNAE2c"
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    client_secrets_file = []
    api_service_name = "youtube"
    api_version = "v3"
    for i in range(0, accounts):
        directory = "secret/client_secret_" + str(i) + ".json"
        client_secrets_file.append(directory)

    flow = []
    credentials = []
    youtube = []

    # Get credentials and create an API client
    for i in range(0, accounts):
        flow.append(google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file[i], scopes))
        credentials.append(flow[i].run_console())
        youtube.append(googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials[i]))

    counter = 0
    while True:
        try:
            for i in range(0, accounts):
                list_videos_byid = youtube[i].videos().list(id=video_id,
                                                            part="statistics",
                                                            ).execute()

                # extracting the views number from search response
                results = list_videos_byid.get("items", [])
                views = results[0]["statistics"]["viewCount"]
                views_title = "This video has " + str(views) + " views."

                # Updating the Title of the video

                request = youtube[i].videos().update(
                    part="snippet",
                    body={
                        "id": video_id,

                        "snippet": {
                            "categoryId": 28,
                            "title": views_title
                        },

                    }
                )
                response = request.execute()

                # Updating the Thumbnail
                txtimage.createimage(views)

                youtube[i].thumbnails().set(
                    videoId=video_id,

                    # TODO: For this request to work, you must replace "YOUR_FILE"
                    #       with a pointer to the actual file you are uploading.
                    media_body=MediaFileUpload("final.png")
                ).execute()

                print(response)
                counter += 1
                time.sleep(65)
                print("This was called " + str(counter) + " times.")

        except Exception as e:
            print(e)
            time.sleep(300)


if __name__ == "__main__":
    main()
