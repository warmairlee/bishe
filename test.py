
import urllib.request


src="http://a3.qpic.cn/psb?/V13MPhBm48ppmF/APpPxGKvs0sL.yuTLaREiI1Hvw1EmtczXmhx1YZ.4UA!/m/dDIBAAAAAAAA&ek=1&kp=1&pt=0&bo=OASABwAAAAAAAJ0!&tl=1&vuin=1154882034&tm=1528261200&sce=60-3-3&rf=newphoto&t=5"
src2="http://a1.qpic.cn/psb?/V13MPhBm48ppmF/P8dzAwz0qt.FvU3Uo6nb7UwCJVvkvsNt9aWcAdde4Ro!/m/dPQAAAAAAAAA&ek=1&kp=1&pt=0&bo=VgtABoIUTgsREO8!&tl=1&vuin=1154882034&tm=1528261200&sce=60-3-3&rf=newphoto&t=5"
src3="http://a3.qpic.cn/psb?/V13MPhBm48ppmF/APpPxGKvs0sL.yuTLaREiI1Hvw1EmtczXmhx1YZ.4UA!/m/dDIBAAAAAAAA&ek=1&kp=1&pt=0&bo=OASABwAAAAAAAJ0!&tl=1&vuin=1154882034&tm=1528264800&sce=60-3-3&rf=newphoto"
req = urllib.request.Request(src3)
img = urllib.request.urlopen(req)
f = open("text/textqq/test/1.jpg", "wb")
f.write(img.read())
f.close()
