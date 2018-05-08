using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Navigation : MonoBehaviour
{
    public Camera cam;
    private NavMeshAgent nav;

	void Start ()
    {
        nav = GetComponent<NavMeshAgent> ();
	}
	
	void Update ()
    {
        if (Input.GetMouseButtonDown (0))
        {
            RaycastHit hit;
            Ray ray = cam.ScreenPointToRay (Input.mousePosition);
            if (Physics.Raycast (ray, out hit))
            {
                if (hit.collider.CompareTag ("Terrain"))
                {
                    transform.LookAt (hit.point);
                    nav.destination = hit.point;
                }
            }
        }
	}
}
