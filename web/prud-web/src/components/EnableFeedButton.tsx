import { Button, Tooltip } from "@mui/material";

import { PublishedWithChangesOutlined } from "@mui/icons-material";
import { enableFeed } from "@/util/prud";

interface Props {
  feedId: number;
  refreshFeedsCallback: () => void;
}

const doEnableFeed = (feedId: number, refreshCallback: () => void) => {
  enableFeed(feedId);
  refreshCallback();
};

const EnableFeedButton: React.FC<Props> = ({
  feedId,
  refreshFeedsCallback,
}) => {
  return (
    <Button
      onClick={() => doEnableFeed(feedId, refreshFeedsCallback)}
      className="absolute -left-10"
    >
      <Tooltip title="Re-Enable Feed">
        <PublishedWithChangesOutlined />
      </Tooltip>
    </Button>
  );
};

export default EnableFeedButton;
