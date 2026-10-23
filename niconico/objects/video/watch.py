"""Data models for the watch API response."""

from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

from niconico.objects.video import EssentialVideo


class WatchAPIMeta(BaseModel):
    """Meta data of the watch API response."""

    status: int
    code: str


class MetaTag(BaseModel):
    """Data model of a meta tag."""

    name: str | None = Field(None)
    property_: str | None = Field(None, alias="property")
    content: str


class LinkTag(BaseModel):
    """Data model of a link tag."""

    href: str
    rel: str
    attrs: dict[str, str] | list


class WatchPageMetadata(BaseModel):
    """Data model of the metadata of a watch page."""

    title: str
    meta_tags: list[MetaTag] = Field(..., alias="metaTags")
    link_tags: list[LinkTag] = Field(..., alias="linkTags")
    json_lds: Any = Field(..., alias="jsonLds")


class WatchClient(BaseModel):
    """Data model of the client of the watch API response."""

    nicosid: str | None
    watch_id: str = Field(..., alias="watchId")
    watch_track_id: str = Field(..., alias="watchTrackId")


class CommentLayerComponent(BaseModel):
    """Data model of a component of a comment layer."""

    thread_id: int = Field(..., alias="threadId")
    fork: int
    fork_label: str = Field(..., alias="forkLabel")


class CommentLayer(BaseModel):
    """Data model of a comment layer."""

    index: int
    is_translucent: bool = Field(..., alias="isTranslucent")
    components: list[CommentLayerComponent]


class CommentThread(BaseModel):
    """Data model of a comment thread."""

    id_: int = Field(..., alias="id")
    fork: int
    fork_label: str = Field(..., alias="forkLabel")
    video_id: str = Field(..., alias="videoId")
    is_post_target: bool = Field(..., alias="isPostTarget")
    is_owner_thread: bool = Field(..., alias="isOwnerThread")
    is_184_forced: bool = Field(..., alias="is184Forced")
    label: str
    post_ng_reason: str | None = Field(..., alias="postNgReason")
    sync_buffer_time: int = Field(..., alias="syncBufferTime")


class CommentNgScore(BaseModel):
    """Data model of the NG score of a comment."""

    is_disabled: bool = Field(..., alias="isDisabled")


class CommentNgViewerItem(BaseModel):
    """Data model of an NG viewer item."""

    type_: str = Field(..., alias="type")
    source: str
    registered_at: str = Field(..., alias="registeredAt")


class CommentNgViewer(BaseModel):
    """Data model of an NG viewer."""

    revision: int
    count: int
    items: list[CommentNgViewerItem]


class CommentNg(BaseModel):
    """Data model of the NG settings of comments."""

    ng_score: CommentNgScore = Field(..., alias="ngScore")
    owner: list
    viewer: CommentNgViewer | None


class NvCommentDataTarget(BaseModel):
    """Data model of a target of the NV comment data."""

    id_: str = Field(..., alias="id")
    fork: str


class NvCommentDataParams(BaseModel):
    """Data model of the parameters of the NV comment data."""

    targets: list[NvCommentDataTarget]
    language: str


class NvCommentData(BaseModel):
    """Data model of the NV comment data."""

    thread_key: str | None = Field(..., alias="threadKey")
    server: str
    params: NvCommentDataParams


class CommentAssist(BaseModel):
    """Data model of the comment assist settings."""

    section_duration_sec: int = Field(..., alias="sectionDurationSec")
    min_match_characters: int = Field(..., alias="minMatchCharacters")
    ignore_post_elapsed_time_sec: int = Field(..., alias="ignorePostElapsedTimeSec")
    ignore_comment_ng_score_threshold: int = Field(..., alias="ignoreCommentNgScoreThreshold")
    comment_count_threshold_list: list[list[Any]] = Field(..., alias="commentCountThresholdList")
    button_display_duration_sec: int = Field(..., alias="buttonDisplayDurationSec")
    button_display_offset_sec: int = Field(..., alias="buttonDisplayOffsetSec")


class WatchComment(BaseModel):
    """Data model of the comment settings of the watch API response."""

    threads: list[CommentThread]
    layers: list[CommentLayer]
    ng: CommentNg
    is_attention_required: bool = Field(..., alias="isAttentionRequired")
    nv_comment: NvCommentData = Field(..., alias="nvComment")
    assist: CommentAssist


class WatchGenre(BaseModel):
    """Data model of the genre of the watch API response."""

    key: str
    label: str
    is_immoral: bool = Field(..., alias="isImmoral")
    is_disabled: bool = Field(..., alias="isDisabled")
    is_not_set: bool = Field(..., alias="isNotSet")


class WatchLazy(BaseModel):
    """Data model of the key used to fetch the lazy watch data."""

    auth_key: str = Field(..., alias="authKey")


class WatchMediaVideo(BaseModel):
    """Data model of a video stream of the watch API response."""

    id_: str = Field(..., alias="id")
    is_available: bool = Field(..., alias="isAvailable")
    quality_level: int = Field(..., alias="qualityLevel")
    label: str
    bit_rate: int = Field(..., alias="bitRate")
    width: int
    height: int


class AudioLoudness(BaseModel):
    """Data model of the loudness of an audio stream."""

    type_: str = Field(..., alias="type")
    value: float


class WatchMediaAudioLabel(BaseModel):
    """Data model of the label of an audio stream."""

    quality: str
    bitrate: str


class WatchMediaAudio(BaseModel):
    """Data model of an audio stream of the watch API response."""

    id_: str = Field(..., alias="id")
    is_available: bool = Field(..., alias="isAvailable")
    quality_level: int = Field(..., alias="qualityLevel")
    bit_rate: int = Field(..., alias="bitRate")
    sampling_rate: int = Field(..., alias="samplingRate")
    integrated_loudness: float = Field(..., alias="integratedLoudness")
    true_peak: float = Field(..., alias="truePeak")
    loudness_collection: list[AudioLoudness] = Field(..., alias="loudnessCollection")
    label: WatchMediaAudioLabel


class WatchMediaContents(BaseModel):
    """Data model of the available streams of the watch API response."""

    videos: list[WatchMediaVideo]
    audios: list[WatchMediaAudio]


class WatchMediaHlsOutput(BaseModel):
    """Data model of an output of a pre-issued HLS playlist."""

    asset_unit_names: list[str] = Field(..., alias="assetUnitNames")


class WatchMediaHls(BaseModel):
    """Data model of a pre-issued HLS playlist."""

    url: str
    outputs: list[WatchMediaHlsOutput]
    created_at: str = Field(..., alias="createdAt")
    expired_at: str = Field(..., alias="expiredAt")


class WatchMediaLowDataMode(BaseModel):
    """Data model of the low data mode limits."""

    video_upper_limit: int = Field(..., alias="videoUpperLimit")
    audio_upper_limit: int = Field(..., alias="audioUpperLimit")


class WatchMedia(BaseModel):
    """Data model of the media of the watch API response."""

    contents: WatchMediaContents
    is_storyboard_available: bool = Field(..., alias="isStoryboardAvailable")
    access_right_key: str = Field(..., alias="accessRightKey")
    hls: WatchMediaHls | None
    low_data_mode: WatchMediaLowDataMode = Field(..., alias="lowDataMode")


class WatchJsonLdOwner(BaseModel):
    """Data model of the owner in the JSON-LD metadata."""

    id_: str = Field(..., alias="id")
    type_: str = Field(..., alias="type")
    name: str
    description: str
    icon_url: str = Field(..., alias="iconUrl")


class WatchJsonLdVideoObject(BaseModel):
    """Data model of the video object in the JSON-LD metadata."""

    regions_allowed: Any = Field(..., alias="regionsAllowed")
    expires_at: str | None = Field(..., alias="expiresAt")


class WatchJsonLd(BaseModel):
    """Data model of the JSON-LD metadata."""

    owner: WatchJsonLdOwner | None
    video_object: WatchJsonLdVideoObject = Field(..., alias="videoObject")


class WatchMetadata(BaseModel):
    """Data model of the metadata of the watch API response."""

    json_ld: WatchJsonLd = Field(..., alias="jsonLd")
    gtm: Any


class WatchPaymentCheck(BaseModel):
    """Data model of a payment option of a video."""

    is_enabled: bool = Field(..., alias="isEnabled")
    show_promotion: bool = Field(..., alias="showPromotion")


class WatchPayment(BaseModel):
    """Data model of the payment settings of the watch API response."""

    watchable_user_type: str = Field(..., alias="watchableUserType")
    commentable_user_type: str = Field(..., alias="commentableUserType")
    billing_type: str = Field(..., alias="billingType")
    ppv: WatchPaymentCheck
    admission: WatchPaymentCheck
    continuation_benefit: WatchPaymentCheck = Field(..., alias="continuationBenefit")
    premium: WatchPaymentCheck


class PlayerInitialPlayback(BaseModel):
    """Data model of the initial playback settings."""

    type_: str = Field(..., alias="type")
    position_sec: float | None = Field(None, alias="positionSec")


class WatchPlayerComment(BaseModel):
    """Data model of the comment settings of the player."""

    is_default_invisible: bool = Field(..., alias="isDefaultInvisible")


class WatchPlayer(BaseModel):
    """Data model of the player settings of the watch API response."""

    comment: WatchPlayerComment
    initial_playback: PlayerInitialPlayback | None = Field(..., alias="initialPlayback")
    layer_mode: int = Field(..., alias="layerMode")


class WatchSystem(BaseModel):
    """Data model of the system information of the watch API response."""

    server_time: str = Field(..., alias="serverTime")
    is_stella_alive: bool = Field(..., alias="isStellaAlive")
    channel_gtm_container_id: str | None = Field(..., alias="channelGtmContainerId")


class WatchTagItem(BaseModel):
    """Data model of a tag of the watch API response."""

    name: str
    is_locked: bool = Field(..., alias="isLocked")


class WatchTagEdit(BaseModel):
    """Data model of the tag edit settings."""

    is_editable: bool = Field(..., alias="isEditable")
    uneditable_reason: str | None = Field(..., alias="uneditableReason")
    edit_key: str | None = Field(..., alias="editKey")


class WatchTags(BaseModel):
    """Data model of the tags of the watch API response."""

    items: list[WatchTagItem]
    has_r18_tag: bool = Field(..., alias="hasR18Tag")
    is_published_nicoscript: bool = Field(..., alias="isPublishedNicoscript")
    edit: WatchTagEdit


class WatchVideoCount(BaseModel):
    """Data model of the counters of a video."""

    view: int
    comment: int
    mylist: int
    like: int


class WatchVideoThumbnail(BaseModel):
    """Data model of the thumbnails of a video."""

    normal: str
    middle: str | None
    large: str | None
    player: str
    ogp: str
    short: str | None


class WatchVideoRating(BaseModel):
    """Data model of the rating of a video."""

    is_adult: bool = Field(..., alias="isAdult")


class WatchVideoPermission(BaseModel):
    """Data model of the permissions of a video."""

    is_private: bool = Field(..., alias="isPrivate")
    is_deleted: bool = Field(..., alias="isDeleted")
    is_authentication_required: bool = Field(..., alias="isAuthenticationRequired")
    is_embed_player_allowed: bool = Field(..., alias="isEmbedPlayerAllowed")
    is_gift_allowed: bool = Field(..., alias="isGiftAllowed")
    is_ng_for_vocacolle_app: bool = Field(..., alias="isNgForVocacolleApp")
    rating: WatchVideoRating


class WatchVideo(BaseModel):
    """Data model of the video of the watch API response."""

    id_: str = Field(..., alias="id")
    content_type: str = Field(..., alias="contentType")
    title: str
    description: str
    supplements: list[Any]
    count: WatchVideoCount
    duration: int
    thumbnail: WatchVideoThumbnail
    registered_at: str = Field(..., alias="registeredAt")
    permission: WatchVideoPermission
    has_lyrics: bool = Field(..., alias="hasLyrics")
    is_high_risk_video: bool = Field(..., alias="isHighRiskVideo")
    is_channel_video: bool = Field(..., alias="isChannelVideo")
    is_owned_by_viewer: bool = Field(..., alias="isOwnedByViewer")
    show_owner_menu: bool = Field(..., alias="showOwnerMenu")
    is_liked_by_viewer: bool = Field(..., alias="isLikedByViewer")


class WatchViewer(BaseModel):
    """Data model of the viewer of the watch API response."""

    id_: int = Field(..., alias="id")
    nickname: str
    is_premium: bool = Field(..., alias="isPremium")
    allow_sensitive_contents: bool = Field(..., alias="allowSensitiveContents")


class WatchVideoLive(BaseModel):
    """Data model of a live video of the watch API response."""

    program_id: str = Field(..., alias="programId")
    begin_at: str = Field(..., alias="beginAt")
    end_at: str = Field(..., alias="endAt")


class WatchData(BaseModel):
    """Data model of the data of the watch API response.

    Owner, series and channel information is not included; get it with `VideoWatchClient.get_watch_lazy_data`.
    """

    response_type: str = Field(..., alias="responseType")
    client: WatchClient
    comment: WatchComment
    media: WatchMedia
    player: WatchPlayer
    video: WatchVideo
    genre: WatchGenre
    tags: WatchTags
    lazy: WatchLazy
    system: WatchSystem
    viewer: WatchViewer | None
    video_ads: Any = Field(..., alias="videoAds")
    video_live: WatchVideoLive | None = Field(..., alias="videoLive")
    payment: WatchPayment
    base_video: Any = Field(..., alias="baseVideo")
    metadata: WatchMetadata
    ok_reason: str = Field(..., alias="okReason")


class WatchResponseError(BaseModel):
    """Data model of the error response of the watch API."""

    status_code: int = Field(..., alias="statusCode")
    error_code: str = Field(..., alias="errorCode")
    reason_code: str | None = Field(..., alias="reasonCode")
    deleted_message: str | None = Field(..., alias="deletedMessage")
    publish_scheduled_at: str | None = Field(..., alias="publishScheduledAt")
    data_set: Any = Field(..., alias="dataSet")


class WatchV4Data(BaseModel):
    """Data model of the watch v4 wrapper of the watch API response."""

    data: WatchData


class WatchResponse(BaseModel):
    """Data model of the response of the watch API response."""

    watch_v4: WatchV4Data = Field(..., alias="$watchV4")
    pcweb: Any


class WatchAPIData(BaseModel):
    """Data model of the data of the watch API response."""

    metadata: WatchPageMetadata
    google_tag_manager: Any | None = Field(..., alias="googleTagManager")
    response: WatchResponse


class WatchAPIErrorData(BaseModel):
    """Data model of an error response of the watch API."""

    metadata: WatchPageMetadata
    response: WatchResponseError


T = TypeVar("T")


class WatchAPIResponse(BaseModel, Generic[T]):
    """Data model of the watch API response.

    ref: https://www.nicovideo.jp/watch/<video_id>?responseType=json&nvpcClientVersion=1
    """

    meta: WatchAPIMeta
    data: T


class WatchLazyUserOwnerIcon(BaseModel):
    """Data model of the icon of a user owner."""

    url: str


class WatchLazyUserOwnerFollow(BaseModel):
    """Data model of the viewer's follow state of a user owner."""

    is_followed: bool = Field(..., alias="isFollowed")


class WatchLazyUserOwner(BaseModel):
    """Data model of a user owner of the lazy watch API response."""

    type_: Literal["user"] = Field(..., alias="type")
    visibility: Literal["visible"]
    id_: int = Field(..., alias="id")
    nickname: str
    icon: WatchLazyUserOwnerIcon
    follow: WatchLazyUserOwnerFollow | None
    owned_channel: Any = Field(..., alias="ownedChannel")
    current_live: Any = Field(..., alias="currentLive")
    upcoming_video_live: Any = Field(..., alias="upcomingVideoLive")


class WatchLazyChannelOwnerThumbnail(BaseModel):
    """Data model of the thumbnail of a channel owner."""

    url: str
    small_url: str | None = Field(..., alias="smallUrl")


class WatchLazyChannelOwnerFollow(BaseModel):
    """Data model of the viewer's follow state of a channel owner."""

    is_subscribed: bool = Field(..., alias="isSubscribed")
    is_bookmarked: bool = Field(..., alias="isBookmarked")
    token: str
    token_timestamp: int = Field(..., alias="tokenTimestamp")


class WatchLazyChannelOwner(BaseModel):
    """Data model of a channel owner of the lazy watch API response."""

    type_: Literal["channel"] = Field(..., alias="type")
    visibility: Literal["visible"]
    id_: str = Field(..., alias="id")
    name: str
    is_official_anime: bool = Field(..., alias="isOfficialAnime")
    is_display_ad_banner: bool = Field(..., alias="isDisplayAdBanner")
    thumbnail: WatchLazyChannelOwnerThumbnail
    follow: WatchLazyChannelOwnerFollow | None


class WatchLazyHiddenOwner(BaseModel):
    """Data model of a hidden owner of the lazy watch API response."""

    type_: str = Field(..., alias="type")
    visibility: Literal["hidden"]


class WatchSeriesVideos(BaseModel):
    """Data model of the neighboring videos of a series."""

    prev: EssentialVideo | None
    next_: EssentialVideo | None = Field(..., alias="next")
    first: EssentialVideo | None


class WatchSeries(BaseModel):
    """Data model of a series of the lazy watch API response."""

    id_: int = Field(..., alias="id")
    title: str
    description: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    video: WatchSeriesVideos


class WatchLazyData(BaseModel):
    """Data model of the data of the lazy watch API response."""

    owner: WatchLazyUserOwner | WatchLazyChannelOwner | WatchLazyHiddenOwner | None
    ranking: Any
    series: WatchSeries | None
    waku: Any


class StoryboardImage(BaseModel):
    """Data model of an image of a storyboard."""

    timestamp: int
    url: str


class StoryboardResponse(BaseModel):
    """Data model of the storyboard response.

    ref: https://asset.domand.nicovideo.jp/<id>/storyboard/~~~
    """

    columns: int
    images: list[StoryboardImage]
    interval: int
    rows: int
    thumbnail_height: int = Field(..., alias="thumbnailHeight")
    thumbnail_width: int = Field(..., alias="thumbnailWidth")
    version: str


class NvCommentAPIMeta(BaseModel):
    """Data model of the NV comment API meta."""

    status: int
    error_code: str | None = Field(None, alias="errorCode")


class GlobalComment(BaseModel):
    """Data model of a global comment."""

    id_: str = Field(..., alias="id")
    count: int


class Comment(BaseModel):
    """Data model of a comment."""

    body: str
    commands: list[str]
    id_: str = Field(..., alias="id")
    is_my_post: bool = Field(..., alias="isMyPost")
    is_premium: bool = Field(..., alias="isPremium")
    nicoru_count: int = Field(..., alias="nicoruCount")
    nicoru_id: str | None = Field(None, alias="nicoruId")
    no: int
    posted_at: str = Field(..., alias="postedAt")
    score: int
    source: str
    user_id: str = Field(..., alias="userId")
    vpos_ms: int = Field(..., alias="vposMs")


class NvCommentThread(BaseModel):
    """Data model of an NV comment thread."""

    id_: str = Field(..., alias="id")
    fork: str
    comment_count: int = Field(..., alias="commentCount")
    comments: list[Comment]


class NvCommentAPIData(BaseModel):
    """Data model of the NV comment data."""

    global_comments: list[GlobalComment] = Field(..., alias="globalComments")
    threads: list[NvCommentThread]


class NvCommentAPIResponse(BaseModel):
    """Data model of the NV comment API response.

    ref: https://public.nvcomment.nicovideo.jp/v1/threads
    """

    data: NvCommentAPIData | None
    meta: NvCommentAPIMeta
