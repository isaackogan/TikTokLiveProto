package com.bytedance.android.livesdk.battle.model;

import X.C102440clw;
import X.InterfaceC209468Jq;
import com.bytedance.android.livesdk.model.message.battle.BattleResult;
import com.bytedance.android.livesdkapi.depend.model.live.match.BattleTeamResult;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/* loaded from: classes2.dex */
public final class BattleRecentContribResponse {

    @InterfaceC209468Jq("data")
    public ResponseData data;

    public static final class ResponseData {

        @InterfaceC209468Jq("gift_log_ids")
        public List<String> giftLogIds = new ArrayList();

        @InterfaceC209468Jq("supported_actions")
        public Map<Long, Boolean> supportedActions = C102440clw.LJII();

        @InterfaceC209468Jq("battle_score")
        public Map<Long, BattleResult> battleScore = C102440clw.LJII();

        @InterfaceC209468Jq("team_battle_score")
        public Map<Long, BattleTeamResult> teamBattleScore = C102440clw.LJII();
    }
}
