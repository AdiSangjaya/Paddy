package com.adisangjaya.paddy

import android.app.ProgressDialog
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.adisangjaya.paddy.network.ApiConfig
import com.adisangjaya.paddy.network.responsemodel.Default
import com.bumptech.glide.Glide
import kotlinx.android.synthetic.main.activity_result.*
import kotlinx.android.synthetic.main.activity_result.namahama
import kotlinx.android.synthetic.main.activity_result.perkenalan
import kotlinx.android.synthetic.main.activity_result.penanganan
import okhttp3.MediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Response
import java.io.File

class ResultActivity : AppCompatActivity() {
    lateinit var image: MultipartBody.Part
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_result)

        // mempilkan image yang akan diupload dengan glide ke imgUpload.
        Glide.with(this).load(intent.getStringExtra("IMG")).into(imgResult)

        // mempilkan image yang akan diupload dengan glide ke imgUpload.
        Glide.with(this).load(intent.getStringExtra("IMG")).into(imgResult)

        val requestBody = RequestBody.create(MediaType.parse("multipart"), File(intent.getStringExtra("IMG")))

        // mengoper value dari requestbody sekaligus membuat form data untuk upload. dan juga mengambil nama dari picked image
        image = MultipartBody.Part.createFormData("image", File(intent.getStringExtra("IMG"))?.name,requestBody)

        Result()

        back1.setOnClickListener {
            intent = Intent(this, UploadActivity::class.java)
            startActivity(intent)
        }
        back2.setOnClickListener {
            intent = Intent(this, UploadActivity::class.java)
            startActivity(intent)
        }
    }
    private fun Result(){

        // meampilkan progress dialog
        val loading = ProgressDialog(this)
        loading.setMessage("Please wait...")
        loading.show()

        // init retrofit
        val call = ApiConfig().instance().upload(image)

        // membaut request ke api
        call.enqueue(object : retrofit2.Callback<Default>{

            // handling request saat fail
            override fun onFailure(call: Call<Default>?, t: Throwable?) {
                loading.dismiss()
                Toast.makeText(applicationContext,"Connection error", Toast.LENGTH_SHORT).show()
                Log.d("ONFAILURE",t.toString())
            }

            // handling request saat response.
            override fun onResponse(call: Call<Default>?, response: Response<Default>?) {

                // dismiss progress dialog
                loading.dismiss()

                // menampilkan pesan yang diambil dari response.
                //Toast.makeText(applicationContext,response?.body()?.nm_brg,Toast.LENGTH_SHORT).show()

                namahama.setText(response?.body()?.nama_hama)
                perkenalan.setText(response?.body()?.perkenalan)
                penanganan.setText(response?.body()?.penanganan)
                if (response?.body()?.nama_hama.isNullOrBlank()){
                    namahama.setText("Hama\nBelum tersedia")
                    perkenalan.setText("null")
                    penanganan.setText("null")
                }
            }


        })


    }

}