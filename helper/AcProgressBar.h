//AcProgressBar.h

/************************************************************************
*˵���������ʵ��һ����AutoCAD״̬������ʾ����������
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
  //����
  bool create(ACHAR* strHint , range_t nRangeMin, range_t nRangeMax );
  //����
  void restore();
  //���õ�ǰλ��
  bool setPos(range_t nPos,ACHAR* strHint);
  bool setPos(range_t nPos);
  //�ƶ�
  bool stepIt(range_t nStep = 1){return setPos(mCurPos+nStep);}
  //��ȡ��ǰλ��
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

  //����״̬�����֣�������������
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

  //ɾ��״̬������
  void restoreText()
  {
    setText(NULL);
  }
};
