/* Modifed from https://github.com/shadcn-ui/ui/issues/355#issuecomment-2405553102 */
"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { TreeItem } from "@/lib/types";
import { Icon } from "@iconify-icon/react";

interface TreeNodeProps {
  item: TreeItem;
  parentId?: string | null;
  openId: string | null;
  setOpenId: (openId: string | null) => void;
}

function TreeNode({ item, parentId = null, openId, setOpenId }: TreeNodeProps) {
  const open = !!(openId && openId.startsWith(item.id));
  const hasChildren = item.children && item.children.length > 0;

  return (
    <Collapsible
      open={open}
      onOpenChange={() => {
        if (open) {
          setOpenId(parentId);
        } else {
          setOpenId(item.id);
        }
      }}
    >
      <CollapsibleTrigger asChild>
        <Button
          variant="ghost"
          className={`w-full justify-start px-2 py-1 text-left ${
            parentId === null ? "font-semibold" : ""
          }`}
        >
          {hasChildren && (
            <Icon
              icon="mdi:chevron-down"
              className={`mr-2 h-4 w-4 shrink-0 transition-transform ${
                open ? "rotate-0" : "-rotate-90"
              }`}
            />
          )}
          {item.label}
        </Button>
      </CollapsibleTrigger>
      {hasChildren && (
        <CollapsibleContent className="ml-4">
          {item.children!.map((child) => (
            <TreeNode
              key={child.id}
              item={child}
              parentId={item.id}
              openId={openId}
              setOpenId={setOpenId}
            />
          ))}
        </CollapsibleContent>
      )}
    </Collapsible>
  );
}

interface TreeProps {
  treeData: TreeItem[];
}

export default function Tree({ treeData }: TreeProps) {
  const [openId, setOpenId] = useState<string | null>(null);
  return (
    <>
      {treeData.map((item) => (
        <TreeNode
          key={item.id}
          item={item}
          openId={openId}
          setOpenId={setOpenId}
        />
      ))}
    </>
  );
}
