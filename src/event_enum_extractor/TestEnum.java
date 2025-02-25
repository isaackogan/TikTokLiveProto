package X;

import com.bytedance.android.livesdk.livesetting.gift.LiveComboLongPressTimeGap;
import com.bytedance.android.livesdk.livesetting.level.LevelPrivilegeUnlockBubbleCacheLengthSetting;
import com.bytedance.android.livesdk.livesetting.level.UserLevelGeckoUpdateSetting;
import com.bytedance.android.livesdk.livesetting.other.LiveCommentMuteRuleContentMaxLengthSetting;
import com.ss.ttlivestreamer.livestreamv2.Constants;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

/* renamed from: X.1g7, reason: invalid class name and case insensitive filesystem */
/* loaded from: classes2.dex */
public enum EnumC39151g7 {
    A_I_LIVE_SUMMARY_MESSAGE("WebcastAILiveSummaryMessage", 0),
    A_I_SUMMARY_MESSAGE("WebcastAISummaryMessage", 1),
    ACCESS_CONTROL_MESSAGE("WebcastAccessControlMessage", 2),
    ACCESS_RECALL_MESSAGE("WebcastAccessRecallMessage", 3),
    ACTIVITY_QUIZ_CARD_MESSAGE("WebcastActivityQuizCardMessage", 4),
    ACTIVITY_QUIZ_USER_IDENTITY_MESSAGE("WebcastActivityQuizUserIdentityMessage", 5),
    ANCHOR_GET_SUB_QUOTA_MESSAGE("WebcastAnchorGetSubQuotaMessage", 6),
    ANCHOR_GROW_LEVEL_MESSAGE("WebcastAnchorGrowLevelMessage", 7),
    ANCHOR_REMINDER_WORD_MESSAGE("WebcastAnchorReminderWordMessage", 8),
    ANCHOR_TASK_REMINDER_MESSAGE("WebcastAnchorTaskReminderMessage", 9),
    ANCHOR_TOOL_MODIFICATION_MESSAGE("WebcastAnchorToolModificationMessage", 10),
    ASSET_MESSAGE("WebcastAssetMessage", 11),
    AUDIENCE_RESERVE_USER_STATE_MESSAGE("WebcastAudienceReserveUserStateMessage", 12),
    AUTHORIZATION_NOTIFY_MESSAGE("WebcastAuthorizationNotifyMessage", 13),
    AVATAR_GENERATE_RESULT_MESSAGE("WebcastAvatarGenerateResultMessage", 14),
    AVATAR_REPORT_DELETE_MESSAGE("WebcastAvatarReportDeleteMessage", 15),
    AVATAR_STYLE_RESULT_MESSAGE("WebcastAvatarStyleResultMessage", 16),
    BA_LEAD_GEN("WebcastBALeadGenMessage", 17),
    BA_LINK_FULL_MESSAGE("WebcastBALinkFullMessage", 18),
    BACKPACK_MESSAGE("WebcastBackpackMessage", 19),
    BARRAGE_MESSAGE("WebcastBarrageMessage", 20),
    BIZ_STICKER_MESSAGE("WebcastBizStickerMessage", 21),
    GIFT_BOOST_CARD_MESSAGE("WebcastBoostCardMessage", 22),
    BOOSTED_USERS_MESSAGE("WebcastBoostedUsersMessage", 23),
    BOTTOM_MESSAGE("WebcastBottomMessage", 24),
    CAPSULE_MESSAGE("WebcastCapsuleMessage", 25),
    CAPTION_MESSAGE("WebcastCaptionMessage", 26),
    CHAT("WebcastChatMessage", 27),
    COHOST_RESERVE_MESSAGE("WebcastCohostReserveMessage", 28),
    COHOST_TOPIC_MESSAGE("WebcastCohostTopicMessage", 29),
    COLD_START_MESSAGE("WebcastColdStartMessage", 30),
    COMMENT_TRAY_MESSAGE("WebcastCommentTrayMessage", 31),
    COMMENT_IMAGE("WebcastCommentsMessage", 32),
    COMMERCIAL_CUSTOM_MESSAGE("WebcastCommercialCustomMessage", 33),
    COMMON_POPUP_MESSAGE("WebcastCommonPopupMessage", 34),
    COMMON_TOAST("WebcastCommonToastMessage", 35),
    COMPETITION_MESSAGE("WebcastCompetitionMessage", 36),
    CONTROL("WebcastControlMessage", 37),
    COUNTDOWN_FOR_ALL_MESSAGE("WebcastCountdownForAllMessage", 38),
    COUNTDOWN_MESSAGE("WebcastCountdownMessage", 39),
    DIGG("WebcastDiggMessage", 40),
    DONATION_INFO("WebcastDonationInfoMessage", 41),
    DONATION_MESSAGE("WebcastDonationMessage", 42),
    MODIFY_DECORATION("WebcastDonationStickerModifyMethod", 43),
    EC_BARRAGE_MESSAGE("WebcastEcBarrageMessage", 44),
    EC_DRAW_MESSAGE("WebcastEcDrawMessage", 45),
    EC_SHORT_ITEM_REFRESH_MESSAGE("WebcastEcShortItemRefreshMessage", 46),
    EC_TASK_REFRESH_COUPON_LIST_MESSAGE("WebcastEcTaskRefreshCouponListMessage", 47),
    EC_TASK_REGISTER_MESSAGE("WebcastEcTaskRegisterMessage", 48),
    EFFECT_CONTROL_MESSAGE("WebcastEffectControlMessage", 49),
    EFFECT_PRELOADING_MESSAGE("WebcastEffectPreloadingMessage", 50),
    EMOTE_CHAT("WebcastEmoteChatMessage", 51),
    RED_ENVELOPE_MESSAGE("WebcastEnvelopeMessage", 52),
    ENVELOPE_PORTAL_MESSAGE("WebcastEnvelopePortalMessage", 53),
    EPI_MESSAGE("WebcastEpiMessage", 54),
    FANS_EVENT_MESSAGE("WebcastFansEventMessage", 55),
    FEED_USER_ROOM_MONITOR_MESSAGE("WebcastFeedUserRoomMonitorMessage", 56),
    FOLLOW_CARD_MESSAGE("WebcastFollowCardMessage", 57),
    FORCE_FETCH_RECOMMENDATIONS_MESSAGE("WebcastForceFetchRecommendationsMessage", 58),
    GAME_EMOTE_UPDATE_MESSAGE("WebcastGameEmoteUpdateMessage", 59),
    GAME_GUESS_PIN_CARD_MESSAGE("WebcastGameGuessPinCardMessage", 60),
    GAME_GUESS_TOAST_MESSAGE("WebcastGameGuessToastMessage", 61),
    GAME_GUESS_WIDGETS_MESSAGE("WebcastGameGuessWidgetsMessage", 62),
    GAME_MOMENT_MESSAGE("WebcastGameMomentMessage", 63),
    GAME_O_C_R_PING_MESSAGE("WebcastGameOCRPingMessage", 64),
    GAME_RANK_NOTIFY_MESSAGE("WebcastGameRankNotifyMessage", 65),
    GAME_RECOMMEND_CREATE_GUESS_MESSAGE("WebcastGameRecommendCreateGuessMessage", 66),
    GAME_REQ_SET_GUESS_MESSAGE("WebcastGameReqSetGuessMessage", 67),
    GAME_SERVER_FEATURE_MESSAGE("WebcastGameServerFeatureMessage", 68),
    GAME_SETTING_CHANGE_MESSAGE("WebcastGameSettingChangeMessage", 69),
    GIFT_GLOBAL_MESSAGE("WebcastGiftBroadcastMessage", 70),
    GIFT_COLLECTION_UPDATE_MESSAGE("WebcastGiftCollectionUpdateMessage", 71),
    GIFT_DYNAMIC_RESTRICTION_MESSAGE("WebcastGiftDynamicRestrictionMessage", 72),
    GIFT_GALLERY_MESSAGE("WebcastGiftGalleryMessage", 73),
    GIFT_GUIDE_MESSAGE("WebcastGiftGuideMessage", 74),
    GIFT("WebcastGiftMessage", 75),
    GIFT_NOTICE_MESSAGE("WebcastGiftNoticeMessage", 76),
    GIFT_PANEL_UPDATE_MESSAGE("WebcastGiftPanelUpdateMessage", 77),
    GIFT_PROGRESS_MESSAGE("WebcastGiftProgressMessage", 78),
    GIFT_PROMPT_MESSAGE("WebcastGiftPromptMessage", 79),
    GIFT_RECORD_CAPSULE_MESSAGE("WebcastGiftRecordCapsuleMessage", 80),
    GIFT_UNLOCK_MESSAGE("WebcastGiftUnlockMessage", 81),
    GIFT_UPDATE("WebcastGiftUpdateMessage", 82),
    STREAM_GOAL_SERVER_MESSAGE("WebcastGoalUpdateMessage", 83),
    GOODY_BAG_MESSAGE("WebcastGoodyBagMessage", 84),
    GREETING_MESSAGE("WebcastGreetingMessage", 85),
    GROUP_LIVE_MEMBER_NOTIFY_MESSAGE("WebcastGroupLiveMemberNotifyMessage", 86),
    GUESS_QUESTION_AUDIT_MESSAGE("WebcastGuessQuestionAuditMessage", 87),
    GUEST_INVITE_GUIDE_MESSAGE("WebcastGuestInviteGuideMessage", 88),
    GUEST_INVITE_MESSAGE("WebcastGuestInviteMessage", 89),
    GUEST_SHOWDOWN_MESSAGE("WebcastGuestShowdownMessage", 90),
    GUIDE_MESSAGE("WebcastGuideMessage", 91),
    GUIDE_TASK_MESSAGE("WebcastGuideTaskMessage", 92),
    HASHTAG("WebcastHashtagMessage", 93),
    HIGHLIGHT_FRAGMENT_READY_MESSAGE("WebcastHighlightFragementReady", 94),
    HOT_ROOM_MESSAGE("WebcastHotRoomMessage", 95),
    HOURLY_RANK_REWARD_MESSAGE("WebcastHourlyRankRewardMessage", 96),
    IM_DELETE("WebcastImDeleteMessage", 97),
    BANNER_UPDATE("WebcastInRoomBannerEvent", 98),
    IN_ROOM_BANNER_MESSAGE("WebcastInRoomBannerMessage", 99),
    IN_ROOM_BANNER_REFRESH_MESSAGE("WebcastInRoomBannerRefreshMessage", 100),
    INTERACTION_HUB_GOAL_MESSAGE("WebcastInteractionHubGoalMessage", Constants.MSG_REPORT_NETWORK_QUALITY),
    INTERACTIVE_EFFECT_MESSAGE("WebcastInteractiveEffectMessage", 102),
    KARAOKE_QUEUE_LIST_MESSAGE("WebcastKaraokeQueueListMessage", 103),
    KARAOKE_QUEUE_MESSAGE("WebcastKaraokeQueueMessage", 104),
    KARAOKE_RED_DOT_MESSAGE("WebcastKaraokeRedDotMessage", 105),
    KARAOKE_REQ_MESSAGE("WebcastKaraokeReqMessage", 106),
    KARAOKE_SWITCH_MESSAGE("WebcastKaraokeSwitchMessage", 107),
    KARAOKE_YOU_SING_REQ_MESSAGE("WebcastKaraokeYouSingReqMessage", 108),
    LIKE("WebcastLikeMessage", 109),
    LINK_BUSINESS_MESSAGE("WebcastLinkBusinessMessage", 110),
    BASE_LINK_LAYER_MESSAGE("WebcastLinkLayerMessage", 111),
    LINK_LAYOUT_MESSAGE("WebcastLinkLayoutMessage", 112),
    LINK_MESSAGE("WebcastLinkMessage", 113),
    LINK_MIC_AD_MESSAGE("WebcastLinkMicAdMessage", 114),
    LINK_CO_HOST_GUIDE("WebcastLinkMicAnchorGuideMessage", 115),
    LINK_MIC_BATTLE_ARMIES("WebcastLinkMicArmies", 116),
    LINK_MIC_BATTLE("WebcastLinkMicBattle", 117),
    LINK_MIC_BATTLE_ITEM_CARD("WebcastLinkMicBattleItemCard", 118),
    LINK_MIC_BATTLE_PUNISH_FINISH("WebcastLinkMicBattlePunishFinish", 119),
    LINK_MIC_BATTLE_VICTORY_LAP_MESSAGE("WebcastLinkMicBattleVictoryLap", 120),
    LINK_MIC_FAN_TICKET_METHOD("WebcastLinkMicFanTicketMethod", 121),
    LINK_MIC("WebcastLinkMicMethod", 122),
    LINK_MIC_SIGNAL("WebcastLinkMicSignalingMethod", 123),
    LINK_SCREEN_CHANGE_MESSAGE("WebcastLinkScreenChangeMessage", 124),
    LINK_STATE_MESSAGE("WebcastLinkStateMessage", LiveComboLongPressTimeGap.DEFAULT),
    LINKMIC_ANIMATION_MESSAGE("WebcastLinkmicAnimationMessage", 126),
    LINK_AUDIENCE_NOTICE("WebcastLinkmicAudienceNoticeMessage", 127),
    LINK_MIC_BATTLE_NOTICE("WebcastLinkmicBattleNoticeMessage", 128),
    LINK_MIC_BATTLE_TASK("WebcastLinkmicBattleTaskMessage", 129),
    LIVE_EVENT_MESSAGE("WebcastEventMessage", 130),
    LIVE_GAME_INTRO_MESSAGE("WebcastLiveGameIntroMessage", 131),
    LIVE_INFO_AUDIT_NOTICE_MESSAGE("WebcastLiveInfoAuditNoticeMessage", 132),
    LIVE_INTRO_MESSAGE("WebcastLiveIntroMessage", 133),
    LIVE_JOURNEY_MESSAGE("WebcastLiveJourneyMessage", 134),
    LIVE_SHOW_MESSAGE("WebcastLiveShowMessage", 135),
    MARQUEE_ANNOUNCEMENT_MESSAGE("WebcastMarqueeAnnouncementMessage", 136),
    MEMBER("WebcastMemberMessage", 137),
    MIDDLE_TOUCH_MESSAGE("WebcastMiddleTouchMessage", 138),
    MSG_DETECT_MESSAGE("WebcastMsgDetectMessage", 139),
    MULTI_GUEST_PUNISH_CENTER_ACTION_MSG("WebcastMGPunishCenterActionMessage", UserLevelGeckoUpdateSetting.DEFAULT),
    MULTI_GUEST_SUGGEST_MESSAGE("WebcastMultiGuestSuggestMessage", 141),
    NEW_ANCHOR_GUIDE_MESSAGE("WebcastNewAnchorGuideMessage", 142),
    REMIND("WebcastNoticeMessage", 143),
    NOTICEBOARD_MESSAGE("WebcastNoticeboardMessage", 144),
    NOTICEBOARD_REVIEW_MESSAGE("WebcastNoticeboardReviewMessage", 145),
    ROOM_NOTIFY("WebcastRoomNotifyMessage", 146),
    OFFICIAL_CHANNEL_ANCHOR_MESSAGE("WebcastOChannelAnchorMessage", 147),
    OFFICIAL_CHANNEL_MODIFY_MESSAGE("WebcastOChannelModifyMessage", 148),
    OFFICIAL_CHANNEL_USER_MESSAGE("WebcastOChannelUserMessage", 149),
    OEC_LIVE_HOT_ROOM_MESSAGE("WebcastOecLiveHotRoomMessage", LiveCommentMuteRuleContentMaxLengthSetting.DEFAULT),
    OEC_LIVE_MANAGER_MESSAGE("WebcastOecLiveManagerMessage", 151),
    OEC_LIVE_SHOPPING_MESSAGE("WebcastOecLiveShoppingMessage", 152),
    PAID_CONTENT_LIVE_SHOPPING_MESSAGE("WebcastPaidContentLiveShoppingMessage", 153),
    PARTNERSHIP_CARD_CHANGE_MESSAGE("WebcastPartnershipCardChangeMessage", 154),
    PARTNERSHIP_DOWNLOAD_COUNT_MESSAGE("WebcastPartnershipDownloadCountMessage", 155),
    PARTNERSHIP_DROPS_ANCHOR_MESSAGE("WebcastPartnershipDropsAnchorMessage", 156),
    PARTNERSHIP_DROPS_CARD_CHANGE_MESSAGE("WebcastPartnershipDropsCardChangeMessage", 157),
    PARTNERSHIP_DROPS_UPDATE_MESSAGE("WebcastPartnershipDropsUpdateMessage", 158),
    PARTNERSHIP_GAME_OFFLINE_MESSAGE("WebcastPartnershipGameOfflineMessage", 159),
    PARTNERSHIP_PUNISH_MESSAGE("WebcastPartnershipPunishMessage", 160),
    PARTNERSHIP_TASK_SHOW_MESSAGE("WebcastPartnershipTaskShowMessage", 161),
    PERCEPTION_MESSAGE("WebcastPerceptionMessage", LevelPrivilegeUnlockBubbleCacheLengthSetting.DEFAULT),
    DRAW_GUESS_END_MESSAGE("WebcastPictionaryEndMessage", 163),
    DRAW_GUESS_EXIT_MESSAGE("WebcastPictionaryExitMessage", 164),
    DRAW_GUESS_START_MESSAGE("WebcastPictionaryStartMessage", 165),
    DRAW_GUESS_UPDATE_MESSAGE("WebcastPictionaryUpdateMessage", 166),
    PIN_MESSAGE("WebcastRoomPinMessage", 167),
    PLAY_TOGETHER_MESSAGE("WebcastPlayTogetherMessage", 168),
    PLAYBOOK_MESSAGE("WebcastPlaybookMessage", 169),
    LIVE_POLL_MESSAGE("WebcastPollMessage", 170),
    POPULAR_CARD_MESSAGE("WebcastPopularCardMessage", 171),
    PORTAL_MESSAGE("WebcastPortalMessage", 172),
    PREVIEW_GAME_MOMENT_MESSAGE("WebcastPreviewGameMomentMessage", 173),
    PRIVILEGE_ADVANCE_MESSAGE("WebcastPrivilegeAdvanceMessage", 174),
    PRIVILEGE_DYNAMIC_EFFECT_MESSAGE("WebcastPrivilegeDynamicEffectMessage", 175),
    D_H5_MESSAGE("WebcastProjectDModifyH5", 176),
    PROMOTE_AD_STATUS_MESSAGE("WebcastPromoteAdStatusMessage", 177),
    QUESTION_DELETE_MESSAGE("WebcastQuestionDeleteMessage", 178),
    QUESTION("WebcastQuestionNewMessage", 179),
    QUESTION_SELECT_MESSAGE("WebcastQuestionSelectedMessage", 180),
    QUESTION_SLIDE_DOWN_MESSAGE("WebcastQuestionSlideDownMessage", 181),
    QUESTION_SWITCH_MESSAGE("WebcastQuestionSwitchMessage", 182),
    QUICK_CHAT_LIST_MESSAGE("WebcastQuickChatListMessage", 183),
    RANK_TEXT_MESSAGE("WebcastRankTextMessage", 184),
    RANK_TOAST_MESSAGE("WebcastRankToastMessage", 185),
    RANK_UPDATE_MESSAGE("WebcastRankUpdateMessage", 186),
    REAL_TIME_PERFORMANCE_PAGE_MESSAGE("WebcastRealTimePerformancePageMessage", 187),
    REALTIME_LIVE_CENTER_METHOD("WebcastRealtimeLiveCenterMethod", 188),
    ROOM_PUSH("WebcastRoomBottomMessage", 189),
    ROOM_EVENT_MESSAGE("WebcastRoomEventMessage", 190),
    ROOM("WebcastRoomMessage", 191),
    MODIFY_STICKER("WebcastRoomStickerMessage", 192),
    ROOM_STREAM_ADAPTATION_MESSAGE("WebcastRoomStreamAdaptationMessage", 193),
    USER_SEQ("WebcastRoomUserSeqMessage", 194),
    ROOM_VERIFY("WebcastRoomVerifyMessage", 195),
    SCREEN("WebcastScreenChatMessage", 196),
    SHARE_GUIDE_MESSAGE("WebcastShareGuideMessage", 197),
    SHORT_TOUCH_MESSAGE("WebcastShortTouchMessage", 198),
    SOCIAL("WebcastSocialMessage", 199),
    MODERATOR_OPERATE_MESSAGE("WebcastSpeakerMessage", 200),
    ROOM_RICH_CHAT_MESSAGE("WebcastSpecialPushMessage", 201),
    STAR_COMMENT_NOTIFICATION_MESSAGE("WebcastStarCommentNotificationMessage", 202),
    STAR_COMMENT_PUSH_MESSAGE("WebcastStarCommentPushMessage", 203),
    STREAM_STATUS_MESSAGE("WebcastStreamStatusMessage", 204),
    SUBSCRIPTION_GUIDE_MESSAGE("WebcastSubscriptionGuideMessage", 205),
    SUB_CONTRACT_STATUS_MESSAGE("WebcastSubContractStatusMessage", 206),
    SUB_NOTIFY_MESSAGE("WebcastSubNotifyMessage", 207),
    SUB_PIN_EVENT_MESSAGE("WebcastSubPinEventMessage", 208),
    SUB_QUEUE_MESSAGE("WebcastSubQueueMessage", 209),
    SUB_TIMER_STICKER_MESSAGE("WebcastSubTimerStickerMessage", 210),
    SUB_WAVE_MESSAGE("WebcastSubWaveMessage", 211),
    OPERATE_TOAST_MESSAGE("WebcastToastMessage", 212),
    TRAY_MESSAGE("WebcastTrayMessage", 213),
    LIVE_UNAUTHORIZED_MEMBER_MESSAGE("WebcastUnauthorizedMemberMessage", 214),
    UPGRADE_MESSAGE("WebcastUpgradeMessage", 215),
    USER_STATS("WebcastUserStatsMessage", 216),
    VIDEO_LIVE_COUPON_RCMD_MESSAGE("WebcastVideoLiveCouponRcmdMessage", 217),
    GOODS_ORDER("WebcastVideoLiveGoodsOrderMessage", 218),
    VIDEO_LIVE_GOODS_RCMD_MESSAGE("WebcastVideoLiveGoodsRcmdMessage", 219),
    WALLET_LIVE_REWARDS_RATIO_MESSAGE("WebcastWalletLiveRewardsRatioMessage", 220),
    WALLPAPER_MESSAGE("WebcastWallpaperMessage", 221),
    WALLPAPER_REVIEW_MESSAGE("WebcastWallpaperReviewMessage", 222),
    WEEKLY_RANK_REWARD_MESSAGE("WebcastWeeklyRankRewardMessage", 223),
    WISH_LIST_UPDATE_MESSAGE("WebcastWishlistUpdateMessage", 224),
    DEFAULT("--default--", 225),
    LOCAL_ACTION_MESSAGE("", 226),
    LOCAL_LIVE_PLAY_ORIENTATION_CHANGED_MESSAGE("", 227),
    SYSTEM("", 228),
    DOODLE_GIFT("", 229),
    COMMON_GUIDE("", 230),
    FREE_CELL_GIFT_MESSAGE("", 231),
    BINDING_GIFT_MESSAGE("", 232),
    STREAM_GOAL_ACHIEVE_MESSAGE("", 233),
    CEREMONY_MESSAGE("", 234);

    public static final java.util.Map<String, EnumC39151g7> MESSAGE_MAP = new HashMap();
    public final Class<? extends AbstractC86363a4> messageClass;
    public final String wsMethod;

    public int getIntType() {
        return ordinal();
    }

    static {
        for (EnumC39151g7 enumC39151g7 : values()) {
            MESSAGE_MAP.put(enumC39151g7.wsMethod, enumC39151g7);
        }
    }

    public String getWsMethod() {
        return this.wsMethod;
    }

    public static Class<? extends AbstractC86363a4> getMessageClass(String str) {
        java.util.Map<String, EnumC39151g7> map = MESSAGE_MAP;
        if (map.containsKey(str)) {
            return map.get(str).messageClass;
        }
        return null;
    }

    public static List<EnumC39151g7> getMessageTypes(List<String> list) {
        if (list != null && !list.isEmpty()) {
            ArrayList arrayList = new ArrayList(list.size());
            for (EnumC39151g7 enumC39151g7 : values()) {
                if (list.contains(enumC39151g7.wsMethod)) {
                    arrayList.add(enumC39151g7);
                }
            }
            return arrayList;
        }
        return Collections.emptyList();
    }

    public static EnumC39151g7 valueOf(String str) {
        return (EnumC39151g7) C233219Cz.LIZ(EnumC39151g7.class, str);
    }

    EnumC39151g7(String str, int i) {
        this.messageClass = r1;
        this.wsMethod = str;
    }
}
