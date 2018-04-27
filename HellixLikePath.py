import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

LisCen = IN[0]
LisRad = IN[1]
TopCirRad = IN[2]
SideCurveRad = IN[3]
GenPath = IN[4]

X = Vector.XAxis()
Z = Vector.ZAxis()
co = -1
Pts = []
SideArchs = []

FinalPts = []

if GenPath == True:
	for i in LisCen:
		co = co+1
		Rad = LisRad[co]
		Cen = LisCen[co]
		VecRad = Vector.Scale(X, Rad)
		PtOnCir = Geometry.Translate(Cen, VecRad)
		Pts.append(PtOnCir)
		TopVec = Vector.Scale(Z, Rad*1.3)
		TopPt = Geometry.Translate(Cen, TopVec)
		refAxe = Line.ByStartPointEndPoint(Cen, TopPt)
		
		TopRadVec = Vector.Scale(X, Rad*TopCirRad)
		PtOnTopCir = Geometry.Translate(TopPt, TopRadVec)
		
		SideLine = Line.ByStartPointEndPoint(TopPt, PtOnCir)
		MidSide = Line.PointAtParameter(SideLine, 0.5)
		
		SideVec = Vector.Scale(X, Rad*SideCurveRad)
		PtSide = Geometry.Translate(MidSide, SideVec)
		
		RefArch = Arc.ByThreePoints(PtOnTopCir, PtSide, PtOnCir)
		SideArchs.append(RefArch)
		
		#CreatingHelix
		LayHe = 2
		
		Height = refAxe.Length
		NUmTurn = (Height/2)*360
		
		HelCrv = Helix.ByAxis(Cen, Z, PtOnCir, 2, NUmTurn)
		StPt = Curve.PointAtParameter(HelCrv, 0.0)
		EdPt = Curve.PointAtParameter(HelCrv, 1.0)
		BottCir = Circle.ByCenterPointRadius(Cen, Rad)
		CirLen = BottCir.Length
		HelLen = HelCrv.Length
		NumDiv = (CirLen+HelLen)/LayHe*1/2
		#PtsOnHel = Curve.DivideEqually(HelCrv, NumDiv)
		PtsOnHel = Curve.PointsAtEqualChordLength(HelCrv, NumDiv)
		
		DivPts = []
		DivPts.extend([StPt])
		DivPts.extend(PtsOnHel)
		DivPts.extend([EdPt])
		
		PtsOnHelDome = []
		IntLines = []
		PtsOnArch = []
		FinalPts.append(PtsOnHelDome)
		#PointsOnRefLine 
		for n in DivPts:
			PtOnRefAxe = Geometry.ClosestPointTo(refAxe, n)
			DirVec = Vector.ByTwoPoints(PtOnRefAxe, n)
			DirVec = Vector.Normalized(DirVec)
			intVec = Vector.Scale(X, Rad*2)
			OtherPt = Geometry.Translate(PtOnRefAxe, intVec)
			IntLine = Line.ByStartPointEndPoint(PtOnRefAxe,OtherPt)
			IntLines.append(IntLine)
			PtOnArch = Geometry.Intersect(RefArch, IntLine)
			PtsOnArch.append(PtOnArch)
			DisTOSide = Geometry.DistanceTo(PtOnRefAxe, PtOnArch[0])
			HelVec = Vector.Scale(DirVec, DisTOSide)
			PtOnHelDome = Geometry.Translate(PtOnRefAxe, HelVec)
			PtsOnHelDome.append(PtOnHelDome)
		
	
	

#Assign your output to the OUT variable.
OUT = FinalPts