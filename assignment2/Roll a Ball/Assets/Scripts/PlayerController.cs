using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerController : MonoBehaviour 
{
	public float speed;
	public Text countText;
	public Text winText;
	public Text timerText;
	private Rigidbody rb;
	private int count;
	private float seconds;
	private float minutes;
	private bool gameWon;

	void Start()
	{
		rb = GetComponent<Rigidbody> ();
		count = 0;
		winText.text = "";
		SetCountText ();
		seconds = 0;
		minutes = 0;
		gameWon = false;
	}

	void FixedUpdate()
	{
		if (!gameWon)
		{
			updateTimer ();
		}

		var moveHorizontal = Input.GetAxis ("Horizontal");
		var moveVertical = Input.GetAxis ("Vertical");

		var move = new Vector3 (moveHorizontal, 0.0f, moveVertical);

		rb.AddForce (move * speed);

		var jump = Input.GetAxis ("Jump");
		if (jump > 0 && transform.position.y == 0.5)
			rb.AddForce (new Vector3 (0.0f, 150f, 0.0f));
	}

	void OnTriggerEnter(Collider other) 
	{
		if (other.gameObject.CompareTag ("Pick Up"))
		{
			other.gameObject.SetActive (false);
			count++;
			SetCountText ();
		}
	}

	void SetCountText ()
	{
		countText.text = "Count: " + count.ToString ();
		if (count >= 12)
		{
			winText.text = "You Win!";
			gameWon = true;
		}
	}

	void updateTimer()
	{
		seconds += Time.deltaTime;
		if (seconds > 59) 
		{
			seconds -= 59;
			minutes++;
		}
		timerText.text = minutes.ToString ("00") + ":" + seconds.ToString ("00");
	}
}
