package com.adisangjaya.paddy.network.responsemodel
import com.google.gson.annotations.SerializedName

data class Default (
    @SerializedName("Nama_Hama")
    var nama_hama:String?,
    @SerializedName("Perkenalan_Singkat")
    var perkenalan:String?,
    @SerializedName("Penanganan")
    var penanganan:String?
)