from instagram import instagram
import argparse
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True, help="Instagram username")
ap.add_argument("-p", "--password", required=True, help="Instagram password")
ap.add_argument("-l", "--limit", type=int, required=False, help="Maximum count of likes", default=None)

# TODO : add infinite option

args = vars(ap.parse_args())

max_like = args["limit"]

bot = instagram.Instagram(args["username"], args["password"])

if not bot.login():
    print "! Cannot login into {} account".format(args["username"])
    sys.exit(1)

print "~ Logged in {}".format(args["username"])

liked_items = 0
max_id = ""
loading = True

try:
    while loading:
        feeds = bot.timeline(max_id=max_id)
        if feeds["status"] != "ok":
            print "Can not fetch feeds"
            print feeds["status"]
            break

        for feed in feeds["items"]:
            if feed["has_liked"] and not max_like:
                print "~ All of not liked media finished !"
                loading = False
                break

            print "~ Sending like request for {}.{} ... ".format(feed["id"], feed["user"]["username"]),

            if feed["has_liked"]:
                print "Skipped !"
                continue

            result = bot.like(feed["id"])
            if result["status"] == "ok":
                print "Done !"
                liked_items += 1
            else:
                print "Error !"
                print result["status"]
                loading = False
                break

        if max_like and feeds["more_available"]:
            if liked_items < max_like:
                max_id = feeds["next_max_id"]
                print "~ Next step for {} ".format(max_id)
            else:
                print "~ {} Liked".format(max_like)
                break
except KeyboardInterrupt:
    print "! KeyboardException"
    pass

print "~ Logging out ..."
bot.logout()
