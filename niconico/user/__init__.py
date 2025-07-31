"""This module provides a class that represents a user client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import requests

from niconico.base.client import BaseClient
from niconico.decorators import login_required
from niconico.objects.nvapi import (
    CreateMylistData,
    FeedData,
    FollowingMylistsData,
    MylistData,
    NvAPIResponse,
    OwnSeriesData,
    OwnUserData,
    OwnVideosData,
    RecommendData,
    RelationshipUsersData,
    SeriesData,
    UserData,
    UserMylistsData,
    UserSeriesData,
    UserVideosData,
)
from niconico.user.search import UserSearchClient
from niconico.utils import add_optional_param

if TYPE_CHECKING:
    from niconico.niconico import NicoNico
    from niconico.objects.user import (
        NicoUser,
        OwnNicoUser,
        UserMylistItem,
        UserSeriesItem,
        UserVideosSortKey,
        UserVideosSortOrder,
    )
    from niconico.objects.video import Mylist, MylistSortKey, MylistSortOrder

class UserClient(BaseClient):
    """A class that represents a user client."""

    search: UserSearchClient

    def __init__(self, niconico: NicoNico) -> None:
        """Initialize the client."""
        super().__init__(niconico)
        self.search = UserSearchClient(niconico)

    def get_user(self, user_id: str) -> NicoUser | None:
        """Get a user by its ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            NicoUser | None: The user object if found, None otherwise.
        """
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.user
        return None

    def get_user_followers(self, user_id: str, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followers of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of followers to get per page.
            page (int): The page number to get the followers from.

        Returns:
            RelationshipUsersData | None: The list of followers if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/followed-by/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_user_followings(self, user_id: str, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followings of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of followings to get per page.
            page (int): The page number to get the followings from.

        Returns:
            RelationshipUsersData | None: The list of followings if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/following/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_user_videos(
        self,
        user_id: str,
        *,
        sort_key: UserVideosSortKey = "registeredAt",
        sort_order: UserVideosSortOrder = "asc",
        page_size: int = 30,
        page: int = 1,
        sensitive_contents: Literal["mask", "filter"] | None = None,
    ) -> UserVideosData | None:
        """Get the videos of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            sort_key (UserVideosSortKey): The key to sort the videos by.
            sort_order (UserVideosSortOrder): The order to sort the videos by.
            page_size (int): The number of videos to get per page.
            page (int): The page number to get the videos from.
            sensitive_contents (Literal["mask", "filter"] | None): The sensitive contents to get.

        Returns:
            UserVideosData | None: The list of videos if found, None otherwise.
        """
        query = {
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_contents is not None:
            query["sensitiveContents"] = sensitive_contents
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v3/users/{user_id}/videos?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserVideosData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_user_mylists(self, user_id: str, *, sample_item_count: int = 0) -> list[UserMylistItem]:
        """Get the mylists of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            sample_item_count (int): The number of items to get from each mylist.

        Returns:
            list[UserMylistItem]: The list of mylists if found, an empty list otherwise.
        """
        query = {"sampleItemCount": str(sample_item_count)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/mylists?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylists
        return []

    def get_user_series(self, user_id: str, *, page_size: int = 100, page: int = 1) -> list[UserSeriesItem]:
        """Get the series of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of series to get per page.
            page (int): The page number to get the series from.

        Returns:
            list[UserSeriesData] | None: The list of series if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/series?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserSeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    @login_required()
    def get_own(self) -> OwnNicoUser | None:
        """Get the own user.

        Returns:
            OwnNicoUser | None: The own user object if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v1/users/me")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnUserData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.user
        return None

    @login_required()
    def get_own_followers(self, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followers of the own user.

        Args:
            page_size (int): The number of followers to get per page.
            page (int): The page number to get the followers from.

        Returns:
            RelationshipUsersData | None: The list of followers if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/followed-by/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_followings(self, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followings of the own user.

        Args:
            page_size (int): The number of followings to get per page.
            page (int): The page number to get the followings from.

        Returns:
            RelationshipUsersData | None: The list of followings if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/following/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def follow_user(self, user_id: str) -> bool:
        """Follow a user.

        Args:
            user_id (str): The ID of the user to follow.

        Returns:
            bool: True if the user was successfully followed, False otherwise.
        """
        res = self.niconico.post(f"https://user-follow-api.nicovideo.jp/v1/user/followees/niconico-users/{user_id}.json")
        return res.status_code == requests.codes.ok

    @login_required()
    def unfollow_user(self, user_id: str) -> bool:
        """Unfollow a user.

        Args:
            user_id (str): The ID of the user to unfollow.

        Returns:
            bool: True if the user was successfully unfollowed, False otherwise.
        """
        res = self.niconico.delete(f"https://user-follow-api.nicovideo.jp/v1/user/followees/niconico-users/{user_id}.json")
        return res.status_code == requests.codes.ok

    @login_required()
    def get_own_videos(
        self,
        *,
        sort_key: UserVideosSortKey = "registeredAt",
        sort_order: UserVideosSortOrder = "asc",
        page_size: int = 30,
        page: int = 1,
        sensitive_contents: Literal["mask", "filter"] | None = None,
    ) -> OwnVideosData | None:
        """Get the own videos.

        Args:
            sort_key (UserVideosSortKey): The key to sort the videos by.
            sort_order (UserVideosSortOrder): The order to sort the videos by.
            page_size (int): The number of videos to get per page.
            page (int): The page number to get the videos from.
            sensitive_contents (Literal["mask", "filter"] | None): The sensitive contents to get.

        Returns:
            OwnVideosData | None: The list of own videos if found, None otherwise.
        """
        query = {
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_contents is not None:
            query["sensitiveContents"] = sensitive_contents
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/users/me/videos?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnVideosData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_mylist(
        self,
        mylist_id: str,
        *,
        page_size: int = 20,
        page: int = 1,
    ) -> Mylist | None:
        """Get a own mylist by its ID.

        Args:
            mylist_id (str): The ID of the mylist.
            page_size (int): The number of videos to get per page.
            page (int): The page number.

        Returns:
            Mylist | None: The mylist object if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[MylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylist
        return None

    @login_required()
    def get_own_mylists(self, *, sample_item_count: int = 0) -> list[UserMylistItem]:
        """Get the own mylists.

        Args:
            sample_item_count (int): The number of items to get from each mylist.

        Returns:
            list[UserMylistItem]: The list of own mylists if found, an empty list otherwise.
        """
        query = {"sampleItemCount": str(sample_item_count)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/mylists?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylists
        return []

    @login_required()
    def add_mylist_item(self, mylist_id: str, item_id: str) -> bool:
        """Add a video to a mylist.

        Args:
            mylist_id (str): The ID of the mylist to add the video to.
            item_id (str): The ID of the video to add to the mylist.

        Returns:
            bool: True if the video was successfully added, False otherwise.
        """
        res = self.niconico.post(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}/items?itemId={item_id}")
        return res.status_code == requests.codes.created

    @login_required()
    def remove_mylist_items(self, mylist_id: str, item_ids: list[str]) -> bool:
        """Remove multiple videos from a mylist.

        Args:
            mylist_id (str): The ID of the mylist to remove the videos from.
            item_ids (list[str]): The IDs of the videos to remove from the mylist.

        Returns:
            bool: True if the videos were successfully removed, False otherwise.
        """
        item_ids_str = ",".join(item_ids)
        res = self.niconico.delete(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}/items?itemIds={item_ids_str}")
        return res.status_code == requests.codes.ok

    @login_required()
    def create_mylist(
        self,
        name: str,
        description: str = "",
        *,
        is_public: bool = False,
        default_sort_key: MylistSortKey = "addedAt",
        default_sort_order: MylistSortOrder = "desc",
    ) -> CreateMylistData | None:
        """Create a new mylist.

        Args:
            name (str): The name of the mylist.
            description (str): The description of the mylist.
            is_public (bool): Whether the mylist is public.
            default_sort_key (MylistSortKey): The default sort key for the mylist.
            default_sort_order (MylistSortOrder): The default sort order for the mylist.

        Returns:
            CreateMylistData | None: The created mylist data if successful, None otherwise.
        """
        data = {
            "name": name,
            "description": description,
            "isPublic": "true" if is_public else "false",
            "defaultSortKey": default_sort_key,
            "defaultSortOrder": default_sort_order,
        }
        res = self.niconico.post("https://nvapi.nicovideo.jp/v1/users/me/mylists", data=data)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[CreateMylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_series(self, series_id: str, *, page_size: int = 100, page: int = 1) -> SeriesData | None:
        """Get a own series by its ID.

        Args:
            series_id (str): The ID of the series.
            page_size (int): The number of videos to get per page.
            page (int): The page number.

        Returns:
            SeriesData | None: The series object if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/series/{series_id}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[SeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_series_list(self, *, page_size: int = 100, page: int = 1) -> list[UserSeriesItem]:
        """Get the series list of the own user.

        Args:
            page_size (int): The number of series to get per page.
            page (int): The page number to get the series from.

        Returns:
            list[UserSeriesItem]: The list of series if found, an empty list otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/series?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnSeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    @login_required()
    def get_own_following_mylists(self, *, sample_item_count: int = 0) -> FollowingMylistsData | None:
        """Get the mylists that the own user is following.

        Args:
            sample_item_count (int): The number of items to get from each mylist.

        Returns:
            FollowingMylistsData | None: The following mylists data if found, None otherwise.
        """
        query = {"sampleItemCount": str(sample_item_count)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/following/mylists?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FollowingMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_recommendations(
        self,
        recipe_id: str = Literal["video_watch_recommendation", "video_recommendation_recommend" , "video_top_recommend"],
        *,
        video_id: str | None = None,
        site: str = "nicovideo",
        limit: int | None = None,
        with_reason: bool | None = None,
        sensitive_contents: Literal["mask", "filter"] | None = None,
        recipe_version: int | None = None,
    ) -> RecommendData | None:
        """Get recommendations based on a specific video or general recommendations.

        Args:
            recipe_id (str): The ID of the recommendation recipe.
            video_id (str | None): The ID of the video to base the recommendations on.
            site (str): The site to get recommendations from. Defaults to "nicovideo".
            limit (int | None): The maximum number of recommendations to return.
            with_reason (bool | None): Whether to include reasons for recommendations.
            sensitive_contents (Literal["mask", "filter"] | None):  The sensitive contents to get.
            recipe_version (int | None): The version of the recommendation recipe.

        Returns:
            RecommendData | None: The recommendation data if found, None otherwise.
        """
        query: dict[str, str] = {"recipeId": recipe_id, "site": site}

        # Set defaults and add video_id if provided
        if video_id is not None:
            query["videoId"] = video_id
            limit = limit or 25

        # Build query parameters
        add_optional_param(query, "recipeVersion", recipe_version)
        add_optional_param(query, "limit", limit)
        add_optional_param(query, "with_reason", "true" if with_reason else None)
        add_optional_param(query, "sensitiveContents", sensitive_contents)

        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/recommend?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RecommendData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_following_activities(
        self,
        *,
        endpoint: Literal["publish", "video"] = "publish",
        context: Literal["header_timeline", "my_timeline"] = "header_timeline",
        cursor: str | None = None,
    ) -> FeedData | None:
        """Get activities from users you follow.

        Args:
            endpoint (Literal["publish", "video"]): The API endpoint to use.
                - "publish": All types of activities (video, illust, etc.)
                - "video": Video activities only
            context (str): The context for the feed. Currently not affecting results.
            cursor (str | None): The cursor for pagination. If None, gets the latest activities.

        Returns:
            FeedData | None: The feed data if successful, None otherwise.
        """
        base_url = "https://api.feed.nicovideo.jp/v1/activities/followings"
        url = f"{base_url}/{endpoint}"

        query = {"context": context}
        if cursor is not None:
            query["cursor"] = cursor
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])

        res = self.niconico.get(f"{url}?{query_str}")
        if res.status_code == requests.codes.ok:
            return FeedData(**res.json())
        return None

