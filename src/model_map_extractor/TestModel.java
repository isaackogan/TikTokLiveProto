package com.bytedance.android.livesdk.model.message;

import X.InterfaceC209468Jq;
import java.util.LinkedHashMap;
import java.util.Map;

/* loaded from: classes2.dex */
public final class GalleryData {

    @InterfaceC209468Jq("end_time_in_ms")
    public long endTimeInMs;

    @InterfaceC209468Jq("period")
    public long period;

    @InterfaceC209468Jq("progress")
    public Map<Long, TitleData> progress = new LinkedHashMap();

    public static final class TitleData {

        @InterfaceC209468Jq("current_sponsor_id")
        public long currentSponsorId;

        @InterfaceC209468Jq("goal_count")
        public long goalCount;
    }
}
