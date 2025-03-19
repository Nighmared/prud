import {
  Button,
  Divider,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
} from "@mui/material";
import {
  CancelOutlined,
  CheckCircleOutline,
  LanguageOutlined,
  PublishedWithChangesOutlined,
  RssFeedOutlined,
} from "@mui/icons-material";
import { useEffect, useState } from "react";

import ConfirmField from "@/components/ConfirmField";
import EnableFeedButton from "./EnableFeedButton";
import { Feed } from "@/util/prud";
import Link from "next/link";
import { useRouter } from "next/router";

const numberToString = (num: number) => {
  const twodigit = num % 100;
  const onedigit = num % 10;
  if (11 <= twodigit && twodigit <= 13) {
    return num + "th";
  }
  if (onedigit == 1) {
    return num + "st";
  }
  if (onedigit == 2) {
    return num + "nd";
  }
  if (onedigit == 3) {
    return num + "rd";
  }
  return num + "th";
};

interface props {
  feed: Feed;
  userIsAdmin: boolean;
  refreshFeedsCallback: () => void;
}

const FeedContainer: React.FC<props> = ({
  feed,
  userIsAdmin,
  refreshFeedsCallback,
}) => {
  var suffix_string = "Disabled";
  if (!!feed.disabled_until) {
    // add half an hour because core isn't constantly checking and enabling
    // *1000 because date wants a ms timestamp and the one we have is s
    const disabled_until_date = new Date((feed.disabled_until + 1800) * 1000);
    const year = disabled_until_date.getFullYear();
    const month = disabled_until_date.toLocaleString("default", {
      month: "long",
    });
    const day = numberToString(disabled_until_date.getDate());
    const hour = disabled_until_date.getHours();
    const minute = disabled_until_date.getMinutes();
    const show_minute = minute < 10 ? "0" + minute : String(minute);
    suffix_string +=
      " until " +
      hour +
      ":" +
      show_minute +
      " on " +
      day +
      " of " +
      month +
      " " +
      year +
      " ";
  }

  const [showDeleteBox, setShowDeleteBox] = useState(false);

  const wrappedCallback = () => {
    setShowDeleteBox(false);
    refreshFeedsCallback();
  };

  const router = useRouter();

  // console.log(suffix_string);
  return (
    <>
      <ListItem>
        {userIsAdmin && !feed.enabled && (
          <EnableFeedButton
            feedId={feed.id as number}
            refreshFeedsCallback={refreshFeedsCallback}
          />
        )}
        <Tooltip title={feed.enabled ? "Enabled" : suffix_string}>
          <ListItemIcon>
            {feed.enabled ? (
              <CheckCircleOutline
                className={feed.enabled ? "text-green-400" : "text-red-500"}
              />
            ) : (
              <CancelOutlined
                className={feed.enabled ? "text-green-400" : "text-red-500"}
              />
            )}
          </ListItemIcon>
        </Tooltip>
        <Link href={`/feed/${feed.id}`}>
          <ListItemButton>
            <ListItemText>{feed.title}</ListItemText>
          </ListItemButton>
        </Link>
        {/* Find a better way for alignment  */}
        <ListItemText />
        <Tooltip title="Link to RSS Feed">
          <ListItemIcon>
            <a target="_blank" href={feed.feed} rel="noopener noreferrer">
              <RssFeedOutlined className="text-orange-500" />
            </a>
          </ListItemIcon>
        </Tooltip>
        <Tooltip title="Link to Blog Homepage">
          <ListItemIcon>
            <a target="_blank" href={feed.url} rel="noopener noreferrer">
              <LanguageOutlined className="text-blue-500" />
            </a>
          </ListItemIcon>
        </Tooltip>
        <div className="min-w-50 flex flex-row">
          {showDeleteBox && (
            <ConfirmField
              feedId={feed.id}
              refreshFeedsCallback={wrappedCallback}
            />
          )}
          {userIsAdmin && (
            <Tooltip title="Delete Feed">
              <Button
                onClick={() => {
                  setShowDeleteBox(!showDeleteBox);
                }}
              >
                {showDeleteBox ? "⬅️" : "❌"}
              </Button>
            </Tooltip>
          )}
        </div>
      </ListItem>
      <Divider />
    </>
  );
};

export default FeedContainer;
