from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.query_utils import Q
from .forms import JoinForm, secretForm
from .models import Member, secret, receipt
from enter.models import Attend
from .mail import word, mail
import datetime
import os


def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():

            form.save()

            messages.add_message(request, messages.SUCCESS,
                                 '提交成功', extra_tags='joinform')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = JoinForm()
    return render(request, 'join.html', {'form': form})


def join_secret(request):
    """
    填寫保密協議表單
    """
    if request.method == 'POST':
        form = secretForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 '提交成功', extra_tags='secretform')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = secretForm()
    return render(request, 'secretForm.html', {'form': form})


def searchForMember(request):
    """
    給社員們用來查詢自己的繳費情形
    """
    if request.method == 'POST':
        nid = request.POST.get('nid')
        if nid:
            try:
                member = Member.objects.get(nid=nid)
                return render(request, 'searchForMember.html', {'member': member})
            except Member.DoesNotExist:
                return render(request, 'searchForMember.html', {'result': '無搜尋結果'})
    return render(request, 'searchForMember.html', {})


@login_required
def search(request):
    """
    admin搜尋入社表單
    """
    if request.method == 'POST':
        searchTerm = request.POST.get('searchTerm')
        # 搜尋大雜燴 一個關鍵字 全部欄位都搜尋
        members = Member.objects.filter(Q(name__icontains=searchTerm) |
                                        Q(nid__icontains=searchTerm) |
                                        Q(dept__icontains=searchTerm) |
                                        Q(phone__icontains=searchTerm) |
                                        #Q(email__icontains=searchTerm) |
                                        Q(bankAccount__icontains=searchTerm) |
                                        #Q(DiscordId__icontains=searchTerm) |
                                        Q(clothes__icontains=searchTerm)
                                        )
        context = {'members': members}
        return render(request, 'join_search.html', context)
    return render(request, 'join_search.html', {})


@login_required
def secretSearch(request):
    """
    admin搜尋保密協議
    """
    if request.method == 'POST':
        searchTerm = request.POST.get('searchTerm')

        # 搜尋大雜燴 一個關鍵字 全部欄位都搜尋
        secrets = secret.objects.filter(Q(name__icontains=searchTerm) |
                                        Q(nid__icontains=searchTerm) |
                                        Q(phone__icontains=searchTerm))
        try:
            # 條碼機刷學生證會多一位數
            Temp = searchTerm
            if len(searchTerm) == 9:
                Temp = searchTerm[0:-1]
            secretResult = secret.objects.get(nid__iexact=Temp)
            context = {'secret': secretResult, 'secrets': secrets}
            return render(request, 'secret_search.html', context)
        except secret.DoesNotExist:
            context = {'secrets': secrets, 'searchTerm': searchTerm}
            return render(request, 'secret_search.html', context)

    return render(request, 'secret_search.html', {})


@login_required
def send_email(request, id):
    '''
    繳費完成後，寄送收據給社員
    '''
    member = get_object_or_404(Member, id=id)
    path = os.path.join('Receipt', '社費')
    if member.is_FCU == 'N':  # 校外學生
        file1 = os.path.join(path, '社員收執', '11010107' +
                             str(member.receiptNumber).zfill(3) + '.pdf')
        file2 = os.path.join(path, '社團存根', '11010107' +
                             str(member.receiptNumber).zfill(3) + '.pdf')
    else:
        file1 = os.path.join(path, '社員收執', '11010101' +
                             str(member.receiptNumber).zfill(3) + '.pdf')
        file2 = os.path.join(path, '社團存根', '11010101' +
                             str(member.receiptNumber).zfill(3) + '.pdf')
    if os.path.isfile(file1) == False or os.path.isfile(file2) == False:
        if member.receiptNumber == 0:
            Receipt = receipt.objects.all()
            if len(Receipt) == 0:
                receipt.objects.create(FCUcount=0, offFCUcount=0)
                Receipt = receipt.objects.all()
            receiptTmp = Receipt[0]
            if member.is_FCU == 'N':  # 校外學生
                receiptTmp.offFCUcount += 1
                member.receiptNumber = receiptTmp.offFCUcount
            else:
                receiptTmp.FCUcount += 1
                member.receiptNumber = receiptTmp.FCUcount
            receiptTmp.save()
            member.save()
        time_now = datetime.datetime.now().strftime("%Y-%m-%d")
        word(member.name, member.nid, time_now,
             member.receiptNumber, member.is_FCU)

    try:
        mail(member.name, member.nid, member.is_FCU,
             member.email, member.receiptNumber)
    except FileNotFoundError:   # Libre 一次產生大量pdf好像會有BUG 先這樣寫
        return redirect('join:review', id)
    member.status = 'M'  # 社員狀態改為已入社
    member.save()
    return redirect('join:review', id)


@login_required
def review(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        if member.status == 'NP':
            # 先寄送電子收據 再把狀態改為已入社
            return redirect('join:send_email', id)
    return render(request, 'review.html', {'member': member})


@login_required
def edit(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = JoinForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('join:review', args=[member.id]))
        else:
            return render(request, 'join_edit.html', {'form': form, 'member': member})
    else:
        form = JoinForm()
    return render(request, 'join_edit.html', {'form': form, 'member': member})


@login_required
def view(request):
    M_members = Member.objects.filter(status='M')
    NP_members = Member.objects.filter(status='NP')
    attends = Attend.objects.all()
    return render(request, 'view.html', {'M_members': M_members, 'NP_members': NP_members, 'attends': attends})
