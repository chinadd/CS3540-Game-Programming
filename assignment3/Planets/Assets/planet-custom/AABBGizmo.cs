using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AABBGizmo : MonoBehaviour 
{
	private Bounds b;
	private List<Bounds> bs;

	void Start()
	{
	}

	void Update()
	{
	}

	void GetBounds(Transform child)
	{
		b.Encapsulate (child.GetComponent<Renderer> ().bounds);
		if (child.childCount > 0) {
			for (int i = 0; i < child.childCount; i++) {
				GetBounds (child.GetChild (i));
			}
		}
	}

	void GetChildren(Transform child)
	{
		b = new Bounds (child.TransformPoint(child.position), Vector3.zero);
		GetBounds (child);
		bs.Add (b);
		if (child.childCount > 0) {
			for (int i = 0; i < child.childCount; i++) {
				GetChildren(child.GetChild (i));
			}
		}
	}

	void OnDrawGizmos()
	{
		bs = new List<Bounds> ();
		GetChildren(transform);
		Gizmos.color = Color.white;
		foreach (var a in bs) 
		{
			Gizmos.DrawWireCube (transform.position, a.size);
		}
	}
}
