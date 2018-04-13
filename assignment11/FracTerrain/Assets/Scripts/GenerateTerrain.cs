using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenerateTerrain : MonoBehaviour
{
	void Start ()
    {
        List<Vector3> vertices = new List<Vector3> ();
        List<Vector2> uv = new List<Vector2> ();
        List<int> triangles = new List<int> ();
        for (int i = 0; i < 9; i++)
        {
            for (int j = 0; j < 9; j++)
            {
                vertices.Add (new Vector3 (i, 0, j));
                uv.Add (new Vector2 (i, j));
                triangles.Add (0 + i + j);
                triangles.Add (1 + i + j);
                triangles.Add (2 + i + j);
            }
        }

        Mesh m = GetComponent<MeshFilter> ().mesh;
        m.vertices = vertices.ToArray ();
        m.uv = uv.ToArray ();
        m.triangles = triangles.ToArray ();
        m.RecalculateNormals ();
	}
	
	void Update ()
    {
	}
}
