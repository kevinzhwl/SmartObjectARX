//AcProgressBar.h

/************************************************************************
*说明：定义和实现一个与AutoCAD状态栏上显示进度栏的类
*
*
*
*

************************************************************************/

#pragma once

class AcProgressBar
{
public:
  typedef long range_t;
public:
  AcProgressBar();
  ~AcProgressBar();
  //创建
  bool create(ACHAR* strHint , range_t nRangeMin, range_t nRangeMax );
  //重置
  void restore();
  //设置当前位置
  bool setPos(range_t nPos,ACHAR* strHint);
  bool setPos(range_t nPos);
  //移动
  bool stepIt(range_t nStep = 1){return setPos(mCurPos+nStep);}
  //获取当前位置
  int getPos(){return mCurPos;}
  bool isCreated(){return mIsCreated;}
protected:
  int ApplicationDoEvents();

private:
  bool mIsCreated;
  range_t mRangeMin;
  range_t mRangeMax;
  range_t mCurPos;
  const static int INTERNAL_RANGEMAX = 100;
};

class AcStatusBar
{
public:
  AcStatusBar();
  ~AcStatusBar();

  //设置状态栏文字（不带进度条）
  bool setText( ACHAR lpszText )
  {
    int minWidth = 0;
    int maxWidth = 0;
    if (lpszText != NULL)
    {
        CPaintDC dc(acedGetAcadFrame());
        CSize size = dc.GetTextExtent(lpszText);
        maxWidth = size.cx;
    }

    AcApStatusBar* pStatusBar = acedGetApplicationStatusBar();
    AcPane* pPane = pStatusBar->GetPane(2);
    if (lpszText == NULL)
    {
      pPane->SetVisible(FALSE);
    }
    else
    {
      pPane->SetVisible(TRUE);
      pPane->SetMinWidth(minWidth);
      pPane->SetMaxWidth(maxWidth);
      pPane->SetText(lpszText);
    }
    pStatusBar->Update();

    return true;
  }

  //删除状态栏文字
  void restoreText()
  {
    setText(NULL);
  }
};
