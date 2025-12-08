import { Button, Tooltip } from "@mui/material";

import { deleteFeed } from "@/util/prud";

interface Props {
  refreshFeedsCallback: () => void;
  feedId: Number;
}

const doDeleteFeed = (id: number, refreshCallback: () => void) => {
  deleteFeed(id, refreshCallback);
};

const ConfirmField: React.FC<Props> = ({ refreshFeedsCallback, feedId }) => {
  return (
    <Tooltip title="This will delete this feed and all posts associated with it from the DB!">
      <Button
        onClick={() => {
          doDeleteFeed(feedId as number, refreshFeedsCallback);
        }}
        className="text-red-600 border-dotted font-bold border-2 border-red-700 hover:bg-pink-500 hover:text-white"
      >
        Yes I am Sure
      </Button>
    </Tooltip>
  );
};

export default ConfirmField;
