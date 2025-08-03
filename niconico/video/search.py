"""This module provides the video search client."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Literal

import requests

from niconico.base.client import BaseClient
from niconico.objects.nvapi import FacetData, ListSearchData, NvAPIResponse, VideoSearchData
from niconico.objects.video.search import SnapshotSearchResponse

if TYPE_CHECKING:
    from niconico.objects.video.search import (
        FacetItem,
        ListSearchSortKey,
        ListType,
        SnapshotResponseField,
        SnapshotSortKey,
        SnapshotTargetField,
        VideoSearchSortKey,
        VideoSearchSortOrder,
    )


class VideoSearchClient(BaseClient):
    """A class that represents a video search client."""

    def search_videos_by_keyword(
        self,
        keyword: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        page_size: int = 25,
        page: int = 1,
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> VideoSearchData | None:
        """Search videos by a keyword.

        Args:
            keyword (str): The keyword to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            page_size (int): The page size.
            page (int): The page.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            VideoSearchData | None: The search result.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/video?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[VideoSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def search_videos_by_tag(
        self,
        tag: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        page_size: int = 25,
        page: int = 1,
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> VideoSearchData | None:
        """Search videos by a tag.

        Args:
            tag (str): The tag to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            page_size (int): The page size.
            page (int): The page.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            VideoSearchData | None: The search result.
        """
        query = {
            "tag": tag,
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/video?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[VideoSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_facet_by_keyword(
        self,
        keyword: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> list[FacetItem]:
        """Get the number of videos for each genre of videos searched with specified conditions.

        Args:
            keyword (str): The keyword to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            list[FacetItem]: The facet items.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "sortOrder": sort_order,
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/facet?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FacetData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    def search_facet_by_tag(
        self,
        tag: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> list[FacetItem]:
        """Search videos by a tag.

        Args:
            tag (str): The tag to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            list[FacetItem]: The facet items.
        """
        query = {
            "tag": tag,
            "sortKey": sort_key,
            "sortOrder": sort_order,
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/facet?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FacetData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    def search_lists(
        self,
        keyword: str,
        sort_key: ListSearchSortKey = "_hotTotalScore",
        types: list[ListType] | None = None,
        page_size: int = 100,
        page: int = 1,
    ) -> ListSearchData | None:
        """Search lists.

        Args:
            keyword (str): The keyword to search.
            sort_key (ListSearchSortKey): The sort key.
            types (list[ListType]): The types. If None, all types are included.
            page_size (int): The page size.
            page (int): The page.

        Returns:
            ListSearchData | None: The search result.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if types is not None and len(types) == 1:
            query["types"] = types[0]
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/search/list?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[ListSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def _build_filter_params(self, filters: dict[str, dict[str, Any] | list[Any]]) -> list[str]:
        """Build filter parameters for snapshot search.

        Args:
            filters: Filter conditions dictionary.

        Returns:
            List of filter parameter strings.
        """
        filter_params = []
        for field, conditions in filters.items():
            if isinstance(conditions, dict):
                for operator, value in conditions.items():
                    filter_params.append(f"filters[{field}][{operator}]={value}")
            elif isinstance(conditions, list):
                for i, value in enumerate(conditions):
                    filter_params.append(f"filters[{field}][{i}]={value}")
        return filter_params

    def search_videos_snapshot(
        self,
        q: str,
        targets: list[SnapshotTargetField],
        _sort: SnapshotSortKey,
        *,
        fields: list[SnapshotResponseField] | None = None,
        filters: dict[str, dict[str, Any] | list[Any]] | None = None,
        json_filter: dict[str, Any] | None = None,
        _sort_order: VideoSearchSortOrder = "desc",
        _offset: int = 0,
        _limit: int = 10,
        _context: str = "niconico.py",
    ) -> SnapshotSearchResponse | None:
        """Search videos using Snapshot Search API v2.

        Args:
            q (str): Search keyword.
            targets (list[SnapshotTargetField]): Target fields for search
                (e.g., ["title", "description", "tags"]).
            _sort (SnapshotSortKey): Sort key (e.g., "viewCounter").
            fields (list[SnapshotResponseField] | None): Fields to include in response.
            filters (dict | None): Filter conditions.
            json_filter (dict | None): Complex filter conditions using JSON format.
            _sort_order (VideoSearchSortOrder): Sort order ("desc", "asc", "none").
            _offset (int): Offset for pagination.
            _limit (int): Maximum number of results.
            _context (str): Service or application name.

        Returns:
            SnapshotSearchResponse | None: The search result.
        """
        query = {"q": q, "_offset": str(_offset), "_limit": str(_limit), "_context": _context}

        query["targets"] = ",".join(targets)

        if fields is not None:
            query["fields"] = ",".join(fields)

        # Combine sort key and order
        sort_prefix = "" if _sort_order == "asc" else "-"
        if _sort_order == "none":
            query["_sort"] = _sort
        else:
            query["_sort"] = f"{sort_prefix}{_sort}"

        # Handle filters parameter
        filter_params = []
        if filters is not None:
            filter_params = self._build_filter_params(filters)

        # Handle json_filter parameter
        if json_filter is not None:
            query["jsonFilter"] = json.dumps(json_filter, ensure_ascii=False)

        # Build query string
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        if filter_params:
            query_str += "&" + "&".join(filter_params)

        # Make request with User-Agent header
        headers = {"User-Agent": f"{_context} (niconico.py)"}
        url = f"https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search?{query_str}"

        res = requests.get(url, headers=headers, timeout=30)
        if res.status_code == requests.codes.ok:
            response_data = res.json()
            return SnapshotSearchResponse(**response_data)
        return None
