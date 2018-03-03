Shader "Toon" {
  Properties {
    _ToonColor ("Toon Color", Color) = (1,1,1,1)
  }

  SubShader {
    Tags {
      "LightMode"="ForwardBase"
      "Queue"="Geometry"
      "RenderType"="Opaque"
    }

    Pass {
      CGPROGRAM
      #pragma vertex vert
      #pragma fragment frag
      #include "UnityCG.cginc"
      
      struct vertInput {
        float4 pos : POSITION;
        float3 normal : NORMAL;
      };

      struct vertOutput {
        float4 pos : SV_POSITION;
        float3 normal : TEXCOORD0;
      };

      vertOutput vert(vertInput input) {
        vertOutput o;
        o.pos = UnityObjectToClipPos(input.pos);
        o.normal = UnityObjectToWorldNormal(input.normal);
        return o;
      }

      half4 _ToonColor;

      half4 frag(vertOutput output) : COLOR {
          // TODO: update toon to implement toon shading
          half sat = saturate(dot(output.normal, _WorldSpaceLightPos0.xyz));

          if (sat < 0.33)
            sat = 0.25;
          else if (sat > 0.66)
            sat = 0.75;
          else
            sat = 0.5;
          
          half3 intensity = _ToonColor.xyz * sat;

          return half4(intensity , 1.0);
      }
      ENDCG
    }
  }
}
