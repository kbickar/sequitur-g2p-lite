/*
 * $Id: Obstack.hh 1667 2007-06-02 14:32:35Z max $
 *
 * Copyright (c) 2004-2005  RWTH Aachen University
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License Version 2 (June
 * 1991) as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, you will find it at
 * http://www.gnu.org/licenses/gpl.html, or write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110,
 * USA.
 *
 * Should a provision of no. 9 and 10 of the GNU General Public License
 * be invalid or become invalid, a valid provision is deemed to have been
 * agreed upon which comes closest to what the parties intended
 * commercially. In any case guarantee/warranty shall be limited to gross
 * negligent actions or intended actions or fraudulent concealment.
 */

#ifndef _CORE_OBSTACK_HH
#define _CORE_OBSTACK_HH

#include <new>
#include <algorithm>
#include "Assertions.hh"

namespace Core {

template <class T>
class Obstack {
public:
    typedef T Item;
private:
    struct Chunk {
        Chunk *succ ;
        Item *tail, *end ;
        Item data[1];

        size_t size() const {
            return tail - data ;
        }

        size_t room() const {
            return end - tail;
        }

        void truncate(Item *i) {
            while (i < tail) (--tail)->~Item();
            ensure_(tail == i);
        }

        void clear() {
            truncate(data) ;
            ensure(size() == 0) ;
        }
    };

    static const size_t defaultChunkSize_ = 4096 ;
    size_t chunkCapacity_, chunkSize_ ;

    void setChunkSize(size_t s) {
        chunkSize_ = s;
        chunkCapacity_ = (chunkSize_ - sizeof(Chunk)) / sizeof(Item) + 1;
    }

    void adjustChunkCapacity(size_t neededCapacity) {
        while (chunkCapacity_ < neededCapacity)
            setChunkSize(chunkSize_ * 2);
        verify(chunkCapacity_ > 0) ;
        verify(chunkSize_ > sizeof(Chunk)) ;
    }

    Chunk *newChunk(Item *begin, Item *end, size_t spareCapacity = 1);

    void deleteChunk(Chunk *c) {
        c->clear();
        free(c);
    }

    Chunk *current_; /**< current chunk */
    Item  *begin_;   /**< first item in current chunk */

    void provide_(size_t n);

    void provide(size_t n) {
        if (current_->room() < n) provide_(n);
    }

public:
    Obstack(size_t chunkCapacity = 0);

    void clear() {
        Chunk *c, *cs;
        for (c = current_ ; c ; c = cs) {
            cs = c->succ;
            deleteChunk(c);
        }
        current_ = newChunk(0, 0);
        begin_ = 0;
    }

    ~Obstack() {
        Chunk *c, *cs;
        for (c = current_ ; c ; c = cs) {
            cs = c->succ;
            deleteChunk(c);
        }
    }

    void start() {
        begin_ = current_->tail;
    }

    Item *currentBegin() const {
        return begin_;
    }

    Item *currentEnd() const {
        return current_->tail;
    }

    void grow() {
        require(begin_);
        provide(1);
        new(current_->tail++) Item;
    }

    void grow(const Item &i) {
        require(begin_);
        provide(1);
        new(current_->tail++) Item(i);
    }

    void grow(const Item &i, size_t n) {
        require(begin_);
        provide(n);
        current_->tail = uninitialized_fill_n(current_->tail, n, i);
        new(current_->tail++) Item(i);
    }

    void grow(const Item *begin, const Item *end) {
        require(begin_);
        require(begin <= end);
        provide(end - begin);
        current_->tail = uninitialized_copy(begin, end, current_->tail);
    }

    void grow0(const Item *begin, const Item *end) {
        require(begin_);
        require(begin <= end);
        provide(end - begin + 1);
        current_->tail = std::uninitialized_copy(begin, end, current_->tail);
        *current_->tail++ = 0;
    }

    void finish() {
        begin_ = 0;
    }

    Item *add(const Item &i) {
        start();
        grow(i);
        Item *result = currentBegin();
        finish();
        return result;
    }

    Item *add(const Item *begin, const Item *end) {
        start();
        grow(begin, end);
        Item *result = currentBegin();
        finish();
        return result;
    }

    Item *add0(const Item *begin, const Item *end) {
        start();
        grow0(begin, end);
        Item *result = currentBegin();
        finish();
        return result;
    }
};

template <class T>
typename Obstack<T>::Chunk *Obstack<T>::newChunk(Item *begin, Item *end, size_t spareCapacity) {
    adjustChunkCapacity(end - begin + spareCapacity);
    Chunk *c = (Chunk*) ::malloc(chunkSize_) ;
    hope(c != NULL /* memory allocation failed */);
    c->succ = 0 ;
    c->end  = c->data + chunkCapacity_ ;
    c->tail = std::uninitialized_copy(begin, end, c->data);
    ensure(c->room() >= spareCapacity);
    return c ;
}

template <class T>
void Obstack<T>::provide_(size_t n) {
    Chunk *nc = newChunk(begin_, current_->tail, n) ;
    current_->truncate(begin_);
    begin_ = nc->data;

    if (current_->size() > 0) {
        nc->succ = current_;
    } else {
        nc->succ = current_->succ;
        deleteChunk(current_);
    }
    current_ = nc;

    verify(current_->data <= begin_         &&
           begin_         <= current_->tail &&
           current_->tail <  current_->end) ;

    ensure(current_->room() >= n);
}

template <class T>
Obstack<T>::Obstack(size_t chunkCapacity) {
    setChunkSize(defaultChunkSize_);
    if (chunkCapacity) {
        adjustChunkCapacity(chunkCapacity);
    } else {
        adjustChunkCapacity(1);
    }

    current_ = newChunk(0, 0);
    begin_ = 0;
}



} // namespace Bliss

#endif // _CORE_OBSTACK_HH
