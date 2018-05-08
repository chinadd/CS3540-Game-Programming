using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LoopSubdivision : MonoBehaviour
{
	class MeshHelper {
		public Vector3[] vertices;
		public int[] triangles;
	}

	private MeshHelper mesh1;
	private MeshHelper mesh2;
	private MeshHelper mesh3;
	private MeshHelper mesh4;



	MeshHelper LoopSubdivide(MeshHelper mesh)
	{
		MeshHelper newMesh = new MeshHelper ();


		// TODO: implement Loop subdivision of mesh here
		foreach (var vertex in mesh.vertices)
		{
		}
		newMesh.triangles = (int[])mesh.triangles.Clone();
		newMesh.vertices = (Vector3[])mesh.vertices.Clone();

		return newMesh;
	}

	void Start()
	{
		Mesh mesh = GetComponent<MeshFilter> ().mesh;

		mesh1 = new MeshHelper ();
		mesh1.vertices = mesh.vertices;
		mesh1.triangles = mesh.triangles;

		mesh2 = LoopSubdivide (mesh1);
		mesh3 = LoopSubdivide (mesh2);
		mesh4 = LoopSubdivide (mesh3);

		mesh.RecalculateNormals ();
	}

	void Update ()
	{
		if (Input.GetKeyDown (KeyCode.Alpha1) || Input.GetKeyDown (KeyCode.Alpha2) || Input.GetKeyDown (KeyCode.Alpha3) || Input.GetKeyDown (KeyCode.Alpha4)) {
			Mesh mesh = GetComponent<MeshFilter> ().mesh;
			mesh.Clear ();

			if (Input.GetKeyDown (KeyCode.Alpha1)) {
				mesh.vertices = mesh1.vertices;
				mesh.triangles = mesh1.triangles;
			}
			if (Input.GetKeyDown (KeyCode.Alpha2)) {
				mesh.vertices = mesh2.vertices;
				mesh.triangles = mesh2.triangles;
			}
			if (Input.GetKeyDown (KeyCode.Alpha3)) {
				mesh.vertices = mesh3.vertices;
				mesh.triangles = mesh3.triangles;
			}
			if (Input.GetKeyDown (KeyCode.Alpha4)) {
				mesh.vertices = mesh4.vertices;
				mesh.triangles = mesh4.triangles;
			}

			mesh.RecalculateNormals ();
		}
	}
}
