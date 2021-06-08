from boto3.session import Session

data = [{
        "vpath": "../video1.mp4",
        "ipath": "../cover1.jpg",
        "key": "REUNION",
        "metadata": {"title": "REUNION", "desc": "An explosive train robbery gives McCree the chance to settle some unfinished business with a few former associates in our latest animated short: Reunion!", "cover": "REUNION"}
    }, {
        "vpath": "../video2.mp4",
        "ipath": "../cover2.jpg",
        "key": "SHOOTINGSTAR",
        "metadata": {"title": "SHOOTING STAR", "desc": "We wanted to tell the story of D.Va that no one else knew about. Director Ben Dai and editor Jake Patton take us behind-the-scenes on the making of D.Va's new animated short, SHOOTING STAR.", "cover": "SHOOTINGSTAR"}
    }, {
        "vpath": "../video3.mp4",
        "ipath": "../cover3.jpg",
        "key": "HonorAndGlory",
        "metadata": {"title": "Honor And Glory", "desc": "Explore the origin story of Overwatch's rocket-hammer wielding knight in our latest animated short: Honor and Glory!", "cover": "HonorAndGlory"}
    }, {
        "vpath": "../video4.mp4",
        "ipath": "../cover4.jpg",
        "key": "RiseAndShine",
        "metadata": {"title": "Rise And Shine", "desc": "In 'Rise and Shine', Mei wakes up years after being cryogenically frozen to find that Overwatch has been disbanded, the world is very different than the one she knows, and that she is the last surviving scientist at Ecopoint: Antarctica. With limited resources and time, Mei must use science to figure out a way to get help.", "cover": "RiseAndShine"}
    }, {
        "vpath": "../video5.mp4",
        "ipath": "../cover5.jpg",
        "key": "Infiltration",
        "metadata": {"title": "Infiltration", "desc": "'Infiltration' follows Reaper, Widowmaker, and Sombra as they attempt to assassinate a high-priority target. But, when the operation doesn't go as planned, the Talon agents are forced to improvise... ", "cover": "Infiltration"}
    }, {
        "vpath": "../video6.mp4",
        "ipath": "../cover6.jpg",
        "key": "TheLastBastion",
        "metadata": {"title": "The Last Bastion", "desc": "'The Last Bastion' follows the forgotten battle automaton, Bastion, as it unexpectedly reactivates after laying dormant in the wilderness for over a decade. Fascinated by its unfamiliar surroundings, the curious omnic begins to investigate, but quickly discovers its core combat programming may have a different directive...", "cover": "TheLastBastion"}
    }, {
        "vpath": "../video7.mp4",
        "ipath": "../cover7.jpg",
        "key": "Hero",
        "metadata": {"title": "Hero", "desc": "'Hero' follows the masked vigilante Soldier: 76 on a personal mission to Dorado where he's set to investigate the illegal activities of the Los Muertos gang-but an unexpected complication threatens to compromise his objective.", "cover": "Hero"}
    }, {
        "vpath": "../video8.mp4",
        "ipath": "../cover8.jpg",
        "key": "Dragons",
        "metadata": {"title": "Dragons", "desc": "'Dragons' explores the history of conflict between the scions of the Shimada clan: Hanzo and Genji. In this episode, we follow Hanzo as he returns to the siblings' family home in Hanamura to seek redemption... and confront the ghosts of the past. ", "cover": "Dragons"}
    }, {
        "vpath": "../video9.mp4",
        "ipath": "../cover9.jpg",
        "key": "Alive",
        "metadata": {"title": "Alive", "desc": "'Alive' weaves a tale of Widowmaker, the peerless Talon assassin who stalks her prey with deadly efficiency. In this episode, we spend a fateful night in London's King's Row-where you'll discover how one death can change everything.", "cover": "Alive"}
    }
]


IP = "192.168.0.8"
PORT = "7480"
access_key = "**************"
secret_key = "********************"
host = f"http://{IP}:{PORT}"


session = Session(access_key, secret_key)
client = session.client("s3", endpoint_url=host)

def empty_bucket(client, bucket_name):
    resp = client.list_objects(Bucket=bucket_name)
    assert resp["Name"] == bucket_name
    for obj in resp.get("Contents", []):
        key = obj["Key"]
        client.delete_object(Bucket=bucket_name, Key=key)
        print(f"DELETE Object {key}")

for bucket in client.list_buckets()["Buckets"]:
    bucket_name = bucket["Name"]
    if bucket_name in ["images", "videos"]:
        empty_bucket(client, bucket_name)
        resp = client.delete_bucket(Bucket=bucket_name)
print("Delete all buckets")

for bucket_name in ["images", "videos"]:
    resp = client.create_bucket(Bucket=bucket_name, ACL="public-read")
print("Create new buckets")

for d in data:
    resp = client.put_object(
        Bucket = "videos",
        Key = d["key"],
        ACL = "public-read",
        Metadata = d["metadata"],
        Body = open(d["vpath"], "rb").read()
    )
    resp = client.put_object(
        Bucket = "images",
        Key = d["key"],
        ACL = "public-read",
        Body = open(d["ipath"], "rb").read()
    )
    print(f"PUT Object {d['key']}")

for v in client.list_objects(Bucket="videos")["Contents"]:
    print(v["Key"])






# APIS
## bucket API
"""
# create bucket
# ACL in ["private", "public-read", "public-read-write", "authenticated-read"]
res = client.create_bucket(Bucket="", ACL="public-read")
# delete bucket
res = client.delete_bucket(Bucket="")
# list bucket
res = client.list_buckets(Bucket="")
bucket_list = [bucket["Name"] for bucket in client.list_buckets()["Buckets"]]
# bucket info
res = client.head_bucket(Bucket="")
"""

## object API
""" 
# get object of bucket
res = client.list_objects(Bucket="")
# delete object of bucket
res = client.delete_object(Bucket="", Key="")
# get bucket object
res = client.get_object(Bucket="", Key="")
# get bucket object metadata
res = client.head_object(Bucket="", Key="")
"""

## Get and Put object
"""
resp = client.put_object(
    Bucket = "videos",
    Key = "video1",
    ACL = "public-read",
    Metadata = {"title": "Time-lapse SJTU", "desc": "Time-lapse photography of Shanghai Jiao Tong University landscape", "cover": "sjtu"},
    Body = open("../../video1.mp4", "rb").read()
)

resp = client.get_object(
    Bucket="",
    Key=""
)
with open('sjtu_download.flv', 'wb') as f:
    f.write(resp['Body'].read())
"""
