package com.adisangjaya.paddy.network

import com.adisangjaya.paddy.network.responsemodel.Default
import okhttp3.MultipartBody
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

class ApiConfig{

    companion object {

        // base url dari end point.
        const val BASE_URL = "http://192.168.1.2:5000/"
        const val IMAGE_URL = BASE_URL+"image/"

    }

    // init retrofit
    private fun retrofit() : Retrofit {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    // buat sebuah instance untuk call sebuah interface dari retrofit.
    fun instance() : ApiInterface {

        return retrofit().create(ApiInterface::class.java)
    }
}

// interface dari retrofit
interface ApiInterface{

    @Multipart
    @POST("api/image") // end point dari upload
    fun upload(

        @Part imagename: MultipartBody.Part

    ) : Call<Default> // memanggil response model 'Default'

}