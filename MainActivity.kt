package com.bhasha.ai

import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import java.util.*

class MainActivity : AppCompatActivity() {

    private lateinit var input: EditText
    private lateinit var output: TextView
    private lateinit var meetingSwitch: Switch

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        input = findViewById(R.id.inputText)
        output = findViewById(R.id.resultText)
        meetingSwitch = findViewById(R.id.meetingSwitch)

        findViewById<Button>(R.id.voiceBtn).setOnClickListener { startVoice() }
        findViewById<Button>(R.id.analyzeBtn).setOnClickListener { analyze() }
        findViewById<Button>(R.id.clearBtn).setOnClickListener {
            input.setText("")
            output.text = ""
        }
        findViewById<Button>(R.id.shareBtn).setOnClickListener {
            val share = Intent(Intent.ACTION_SEND)
            share.type = "text/plain"
            share.putExtra(Intent.EXTRA_TEXT, output.text.toString())
            startActivity(Intent.createChooser(share, "Share via"))
        }
    }

    private fun startVoice() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
        )
        startActivityForResult(intent, 101)
    }

    override fun onActivityResult(code: Int, result: Int, data: Intent?) {
        super.onActivityResult(code, result, data)
        if (code == 101 && result == RESULT_OK) {
            input.setText(
                data?.getStringArrayListExtra(
                    RecognizerIntent.EXTRA_RESULTS
                )?.get(0)
            )
        }
    }

    private fun analyze() {
        val text = input.text.toString().lowercase(Locale.getDefault())

        val emotion = when {
            listOf("angry", "mad", "gussa").any { text.contains(it) } -> "Angry"
            listOf("happy", "great", "acha").any { text.contains(it) } -> "Happy"
            listOf("sad", "sorry", "dukhi").any { text.contains(it) } -> "Sad"
            else -> "Neutral"
        }

        val feedback =
            if (meetingSwitch.isChecked)
                "Meeting feedback: stay calm and professional."
            else
                "General tone feedback."

        output.text = """
            Emotion: $emotion
            Mode: ${if (meetingSwitch.isChecked) "Meeting" else "Normal"}
            $feedback
        """.trimIndent()
    }
}